from typing import (
    Any,
    AsyncIterable,
    Awaitable,
    Callable,
    Generic,
    Iterable,
    Literal,
    Optional,
    Sequence,
    TypeVar,
    cast,
    overload,
)

from htmltools import HTML, Tag, TagAttrValue, css

from .. import _utils, reactive
from .._namespaces import resolve_id
from ..session import Session, require_active_session, session_context
from ..types import MISSING, MISSING_TYPE, NotifyException
from ..ui.css import CssUnit, as_css_unit
from ._chat_tokenizer import TokenEncoding, TokenizersEncoding, get_default_tokenizer
from ._chat_types import (
    AssistantMessage,
    ChatMessage,
    UserMessage,
    assistant_message,
    normalize_message,
    normalize_message_chunk,
)
from ._html_deps_py_shiny import chat_deps
from .fill import as_fill_item, as_fillable_container

__all__ = (
    "Chat",
    "chat_ui",
    "ChatMessage",
)

T = TypeVar("T")


SubmitFunction = Callable[[], None]
SubmitFunctionAsync = Callable[[], Awaitable[None]]

# A message formats that can be stored/sent to the chat
FullMessage = ChatMessage | UserMessage | AssistantMessage


class Chat(Generic[T]):
    """
    Create a chat component.

    Creates a chat component for displaying and receiving messages. The chat can be
    used to build conversational interfaces, like chatbots.

    Parameters
    ----------
    id
        A unique identifier for the chat session. In Shiny Core, make sure this id
        matches a corresponding :func:`~shiny.ui.chat_ui` call in the UI.
    messages
        A sequence of messages to display in the chat. Each message can be a
        dictionary with a `content` and `role` key. The `content` key should contain
        the message text, and the `role` key can be "assistant", "user", or "system".
        Note that system messages are not actually displayed in the chat, but will
        still be stored in the chat's `.messages()`.
    tokenizer
        The tokenizer to use for calculating token counts, which is required to impose
        `token_limits` in `.get_messages()`. By default, a pre-trained tokenizer is
        attempted to be loaded the tokenizers library (if available). A custom tokenizer
        can be provided by following the `TokenEncoding` (tiktoken or tozenizer)
        protocol. If token limits are of no concern, provide `None`.
    session
        The :class:`~shiny.Session` instance that the chat should appear in. If not
        provided, the session is inferred via :func:`~shiny.session.get_current_session`.
    """

    def __init__(
        self,
        id: str,
        *,
        messages: Sequence[ChatMessage] = (),
        tokenizer: TokenEncoding | MISSING_TYPE | None = MISSING,
        session: Optional[Session] = None,
    ):

        self.id = id
        self.user_input_id = f"{id}_user_input"

        if isinstance(tokenizer, MISSING_TYPE):
            self._tokenizer = get_default_tokenizer()
        else:
            self._tokenizer = tokenizer

        self._session = require_active_session(session)

        # Chunked messages get accumulated (using this property) before changing state
        self._final_message = ""

        # Keep track of effects so we can destroy them when the chat is destroyed
        self._effects: list[reactive.Effect_] = []

        with session_context(self._session):
            # Initialize message state
            self._messages: reactive.Value[Sequence[FullMessage]] = reactive.Value(())

            # Store (i.e. append) message state and display non-system messages
            for msg in messages:
                _utils.run_coro_sync(self._store_message(msg))
                if msg["role"] != "system":
                    _utils.run_coro_sync(self._send_append_message(msg))

            # When user input is submitted, transform, and store it in the chat state
            # (and make sure this runs before other effects since when the user
            #  calls `.messages()`, they should get the latest user input)
            @reactive.effect(priority=9999)
            async def _store_user_input():
                msg = ChatMessage(content=self.get_user_input(), role="user")
                await self._store_message(msg)

            self._effects.append(_store_user_input)

    def ui(
        self,
        *,
        placeholder: str = "Enter a message...",
        width: CssUnit = "min(680px, 100%)",
        height: CssUnit = "auto",
        fill: bool = True,
        **kwargs: TagAttrValue,
    ) -> Tag:
        """
        Place a chat component in the UI.

        This method is only available in Shiny Express. In Shiny Core, use
        :func:`~shiny.ui.chat_ui` instead.

        Parameters
        ----------
        placeholder
            Placeholder text for the chat input.
        width
            The width of the chat container.
        height
            The height of the chat container.
        fill
            Whether the chat should vertically take available space inside a fillable
            container.
        kwargs
            Additional attributes for the chat container element.
        """

        if not _express_is_active():
            raise RuntimeError(
                "The `ui()` method of the `ui.Chat` class only works in a Shiny Express context."
                " Use `ui.chat_ui()` instead in Shiny Core to locate the chat UI."
            )
        return chat_ui(
            id=self.id,
            placeholder=placeholder,
            width=width,
            height=height,
            fill=fill,
            **kwargs,
        )

    @overload
    def on_user_submit(
        self,
        fn: SubmitFunction | SubmitFunctionAsync,
        *,
        on_error: Literal["sanitize", "actual", "unhandled"] = "sanitize",
    ) -> reactive.Effect_: ...

    @overload
    def on_user_submit(
        self,
    ) -> Callable[[SubmitFunction | SubmitFunctionAsync], reactive.Effect_]: ...

    def on_user_submit(
        self,
        fn: SubmitFunction | SubmitFunctionAsync | None = None,
        *,
        on_error: Literal["sanitize", "actual", "unhandled"] = "sanitize",
    ) -> (
        reactive.Effect_
        | Callable[[SubmitFunction | SubmitFunctionAsync], reactive.Effect_]
    ):
        """
        Define a function to invoke when user input is submitted.

        Apply this method as a decorator to a function (`fn`) that should be invoked when the
        user submits a message. The function should take no arguments.

        In many cases, the implementation of `fn` should do at least the following:
            1. Call `.messages()` to obtain the current chat history.
            2. Generate a response based on those messages.
            3. Append the response to the chat history using `.append_message()` or
              `.append_message_stream()`.

        Parameters
        ----------
        fn
            A function to invoke when user input is submitted.
        on_error
            How to handle errors that occur in response to user input. For options
            1 and 2, the error message is displayed to the user and the app continues
            to run. For option 3, the error message is not displayed, and the app stops:
            - "sanitize": Sanitize the error message before displaying it to the user.
            - "actual": Display the actual error message to the user.
            - "unhandled": Do not display any error message to the user.

        Note
        ----
        This method creates a reactive effect that only gets invalidated when the user
        submits a message. Thus, the function `fn` can read other reactive dependencies,
        but it will only be re-invoked when the user submits a message.
        """

        def create_effect(fn: SubmitFunction | SubmitFunctionAsync):
            afunc = _utils.wrap_async(fn)

            @reactive.effect
            @reactive.event(self.get_user_input)
            async def handle_user_input():
                if on_error == "unhandled":
                    await afunc()
                else:
                    try:
                        await afunc()
                    except Exception as e:
                        await self._remove_loading_message()
                        sanitize = on_error == "sanitize"
                        raise NotifyException(str(e), sanitize=sanitize)

            self._effects.append(handle_user_input)

            return handle_user_input

        if fn is None:
            return create_effect
        else:
            return create_effect(fn)

    def get_messages(
        self,
        *,
        token_limits: tuple[int, int] | None = (4096, 1000),
        apply_user_transform: bool = True,
        apply_assistant_transform: bool = False,
    ) -> Sequence[ChatMessage]:
        """
        Reactively read chat messages

        Obtain the current chat history within a reactive context. Messages are listed
        in the order they were added. As a result, when this method is called in a
        `.on_user_submit()` callback (as it most often is), the last message will be the
        most recent one submitted by the user.

        Parameters
        ----------
        token_limits
            A tuple of two integers. The first integer is the maximum number of tokens
            that can be sent to the model in a single request. The second integer is the
            amount of tokens to reserve for the model's response.
            Can also be `None` to disable message trimming based on token counts.
        apply_user_transform
            Whether to return user input messages with transformation applied. This only
            matters if a `user_input_transform` was provided to the chat constructor.
            This should be `True` when passing the messages to a model for response
            generation, but `False` when you need (to save) the original user input.
        apply_assistant_transform
            Whether to return assistant messages with transformation applied. This only
            matters if an `assistant_response_transform` was provided to the chat
            constructor.

        Returns
        -------
        A sequence of chat messages.
        """

        messages = self._get_trimmed_messages(token_limits=token_limits)

        res: Sequence[ChatMessage] = []
        for m in messages:
            msg = ChatMessage(content=m["content"], role=m["role"])
            if "original_content" in m:
                original = (apply_user_transform and m["role"] == "user") or (
                    apply_assistant_transform and m["role"] == "assistant"
                )
                if original:
                    msg["content"] = m["original_content"]
            res.append(msg)

        return res

    async def append_message(self, message: Any) -> None:
        """
        Append a message to the chat.

        Parameters
        ----------
        message
            The message to append. A variety of message formats are supported including
            a string, a dictionary with `content` and `role` keys, or a relevant chat
            completion object from platforms like OpenAI, Anthropic, Ollama, and others.

        Note
        ----
        Use `.append_message_stream()` instead of this method when `stream=True` (or
        similar) is specified in model's completion method.
        """
        await self._append_message(message)

    async def _append_message(self, message: Any, *, chunk: bool = False) -> None:
        if chunk:
            msg = normalize_message_chunk(message)
            await self._store_message_chunk(msg)
        else:
            msg = normalize_message(message)
            await self._store_message(msg)

        await self._send_append_message(msg, chunk=chunk)

    async def append_message_stream(self, message: Iterable[Any] | AsyncIterable[Any]):
        """
        Append a message as a stream of message chunks.

        Parameters
        ----------
        message
            An iterable or async iterable of message chunks to append. A variety of
            message chunk formats are supported, including a string, a dictionary with
            `content` and `role` keys, or a relevant chat completion object from
            platforms like OpenAI, Anthropic, Ollama, and others.

        Note
        ----
        Use this method (over `.append_message()`) when `stream=True` (or similar) is
        specified in model's completion method.
        """

        message = _utils.wrap_async_iterable(message)

        @reactive.extended_task
        async def _do_stream():
            await self._append_message_stream(message)

        _do_stream()

    async def _append_message_stream(self, message: AsyncIterable[Any]):
        # Start the message
        start = assistant_message(content="")
        start["chunk_type"] = "message_start"
        await self._append_message(start, chunk=True)

        try:
            async for msg in message:
                msg = normalize_message_chunk(msg)
                await self._append_message(msg, chunk=True)
        finally:
            end = assistant_message(content="")
            end["chunk_type"] = "message_end"
            await self._append_message(end, chunk=True)

    # Send a message to the UI
    async def _send_append_message(self, message: FullMessage, chunk: bool = False):
        # print(message)

        if chunk:
            msg_type = "shiny-chat-append-message-chunk"
        else:
            msg_type = "shiny-chat-append-message"

        await self._send_custom_message(msg_type, message)
        # TODO: Joe said it's a good idea to yield here, but I'm not sure why?
        # await asyncio.sleep(0)

    # Store a message in the chat state
    async def _store_message(self, message: FullMessage):
        # First, apply transformers if relevant (& remember the original content)
        original_content = message["content"]
        if message["role"] == "user":
            content = await self.transform_user_input(original_content)
            message = {"content": content, "role": "user"}
            if original_content != content:
                message["original_content"] = original_content  # type: ignore

        if message["role"] == "assistant":
            content = await self.transform_assistant_response(original_content)
            message = {"content": content, "role": "assistant"}
            if original_content != content:
                message["original_content"] = content  # type: ignore
            if isinstance(content, HTML):
                message["content_type"] = "html"  # type: ignore

        # Next, calculate the token count
        if self._tokenizer is not None:
            encoded = self._tokenizer.encode(message["content"])
            if isinstance(encoded, TokenizersEncoding):
                token_count = len(encoded.ids)
            else:
                token_count = len(encoded)
            message["token_count"] = token_count  # type: ignore

        # Get the (current and new) messages
        with reactive.isolate():
            messages = tuple(self._messages()) + (message,)

        self._messages.set(messages)

    def _get_trimmed_messages(
        self,
        *,
        token_limits: tuple[int, int] | None = (4096, 1000),
    ) -> Sequence[FullMessage]:
        messages = self._messages()

        if token_limits is None:
            return messages

        # Can't trim if we don't have token counts
        token_counts = [m.get("token_count", None) for m in messages]
        if None in token_counts:
            return messages

        token_counts = cast(list[int], token_counts)

        # Take the newest messages up to the token limit
        limit, reserve = token_limits
        max_tokens = limit - reserve
        messages2: list[FullMessage] = []
        for i, m in enumerate(reversed(messages)):
            if sum(token_counts[-i - 1 :]) > max_tokens:
                break
            messages2.append(m)

        messages2.reverse()

        return tuple(messages2)

    # For chunk messages, accumulate the chunks until we have a signal that the message
    # has ended
    async def _store_message_chunk(self, msg: AssistantMessage):
        self._final_message += msg["content"]
        if "chunk_type" in msg and msg["chunk_type"] == "message_end":
            final = assistant_message(content=self._final_message)
            await self._store_message(final)
            self._final_message = ""

    def get_user_input(self) -> str:
        """
        Reactively read user input

        Returns
        -------
        The user input message (before any transformation).

        Note
        ----
        Most users shouldn't need to use this method directly since `.messages()`
        contains user input. However, this method can be useful when you need to access
        the un-transformed user input, and/or when you want to take a reactive
        dependency on user input.
        """
        id = self.user_input_id
        return cast(str, self._session.input[id]())

    def set_user_input(self, value: str):
        """
        Set the user input value.

        Parameters
        ----------
        value
            The value to set the user input to.
        """

        _utils.run_coro_sync(
            self._session.send_custom_message(
                "shinyChatMessage",
                {
                    "id": self.id,
                    "handler": "shiny-chat-set-user-input",
                    "obj": value,
                },
            )
        )

    async def transform_user_input(self, input: str) -> str:
        """
        Transform user input before storing it in the chat state.

        A function to transform user input before storing it in the chat `.messages()`
        history. This is useful for implementing RAG workflows, like taking a URL and
        scraping it for text before sending it to the model.

        Parameters
        ----------
        input
            The user input message.

        Returns
        -------
        The transformed user input message.
        """
        return input

    async def transform_assistant_response(self, response: str) -> str | HTML:
        """
        Transform assistant responses before they are displayed in the chat.

        A function to transform role="assistant" messages for display purposes. If the
        function returns a string, it will be interpreted and parsed as a markdown
        string on the client (and the resulting HTML is then sanitized). If the function
        returns HTML, it will be displayed as-is. Note that, for
        `.append_message_stream()`, the transformer will be applied to each message in
        the stream, so it should be performant. By default, assistant responses are
        interpreted as markdown on the client.

        Parameters
        ----------
        response
            The assistant response message.

        Returns
        -------
        The transformed assistant response message.
        """
        return response

    async def clear_messages(self):
        """
        Clear all chat messages.
        """
        self._messages.set(())
        await self._send_custom_message("shiny-chat-clear-messages", None)

    def destroy(self):
        """
        Destroy the chat instance.
        """
        for x in self._effects:
            x.destroy()

    async def _remove_loading_message(self):
        await self._send_custom_message("shiny-chat-remove-loading-message", None)

    async def _send_custom_message(self, handler: str, obj: FullMessage | None):
        await self._session.send_custom_message(
            "shinyChatMessage",
            {
                "id": self.id,
                "handler": handler,
                "obj": obj,
            },
        )


def chat_ui(
    id: str,
    *,
    placeholder: str = "Enter a message...",
    width: CssUnit = "min(680px, 100%)",
    height: CssUnit = "auto",
    fill: bool = True,
    **kwargs: TagAttrValue,
) -> Tag:
    """
    UI container for a chat component (Shiny Core).

    This function is for locating a :class:`~shiny.ui.Chat` instance in a Shiny Core
    app. If you are using Shiny Express, use the :method:`~shiny.ui.Chat.ui` method
    instead.

    Parameters
    ----------
    id
        A unique identifier for the chat UI.
    placeholder
        Placeholder text for the chat input.
    width
        The width of the chat container.
    height
        The height of the chat container.
    fill
        Whether the chat should vertically take available space inside a fillable container.
    kwargs
        Additional attributes for the chat container element.
    """

    id = resolve_id(id)

    res = Tag(
        "shiny-chat-container",
        chat_deps(),
        {
            "style": css(
                width=as_css_unit(width),
                height=as_css_unit(height),
            )
        },
        id=id,
        placeholder=placeholder,
        fill=fill,
        **kwargs,
    )

    if fill:
        res = as_fillable_container(as_fill_item(res))

    return res


def _express_is_active() -> bool:
    from ..express._run import get_top_level_recall_context_manager

    try:
        get_top_level_recall_context_manager()
        return True
    except RuntimeError:
        return False
