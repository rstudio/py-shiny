from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Literal, Optional, TypedDict, Union, cast

from typing_extensions import NotRequired

Role = Literal["assistant", "user", "system"]


class ChatMessage(TypedDict):
    content: str
    role: Role


class ChatMessageChunk(TypedDict):
    content: str
    role: Literal["assistant"]
    type: NotRequired[Literal["message_start", "message_chunk", "message_end"]]


if TYPE_CHECKING:
    from anthropic.types import Message as AnthropicMessage
    from anthropic.types import MessageStreamEvent
    from google.generativeai.types.generation_types import (  # pyright: ignore[reportMissingTypeStubs]
        GenerateContentResponse,
    )
    from langchain_core.messages import BaseMessage, BaseMessageChunk
    from openai.types.chat import ChatCompletion, ChatCompletionChunk


class BaseMessageNormalizer(ABC):
    @abstractmethod
    def normalize(self, message: Any) -> ChatMessage:
        pass

    @abstractmethod
    def normalize_chunk(self, chunk: Any) -> ChatMessageChunk:
        pass

    @abstractmethod
    def can_normalize(self, message: Any) -> bool:
        pass

    @abstractmethod
    def can_normalize_chunk(self, chunk: Any) -> bool:
        pass


class StringNormalizer(BaseMessageNormalizer):
    def normalize(self, message: Any) -> ChatMessage:
        x = cast(Optional[str], message)
        return ChatMessage(content=x or "", role="assistant")

    # Follow openai's convention of "" for message_start and None for message_end
    def normalize_chunk(self, chunk: Any) -> ChatMessageChunk:
        x = cast(Optional[str], chunk)
        type = "message_chunk"
        if x == "":
            type = "message_start"
        if x is None:
            type = "message_end"
            x = ""
        return ChatMessageChunk(content=x, type=type, role="assistant")

    def can_normalize(self, message: Any) -> bool:
        return isinstance(message, str) or message is None

    def can_normalize_chunk(self, chunk: Any) -> bool:
        return isinstance(chunk, str) or chunk is None


class DictNormalizer(BaseMessageNormalizer):
    def normalize(self, message: Any) -> ChatMessage:
        x = cast(dict[str, Any], message)
        if "content" not in x:
            raise ValueError("Message must have 'content' key")
        return ChatMessage(content=x["content"], role=x.get("role", "assistant"))

    def normalize_chunk(self, chunk: Any) -> ChatMessageChunk:
        x = cast(dict[str, Any], chunk)
        if "content" not in x:
            raise ValueError("Chunk must have a 'content' key")
        return ChatMessageChunk(
            content=x["content"],
            role=x.get("role", "assistant"),
            type=x.get("type", None),
        )

    def can_normalize(self, message: Any) -> bool:
        return isinstance(message, dict)

    def can_normalize_chunk(self, chunk: Any) -> bool:
        return isinstance(chunk, dict)


class LangChainNormalizer(BaseMessageNormalizer):
    def normalize(self, message: Any) -> ChatMessage:
        x = cast("BaseMessage", message)
        if isinstance(x.content, list):  # type: ignore
            raise ValueError(
                "The `message.content` provided seems to represent numerous messages. "
                "Consider iterating over `message.content` and calling .append_message() on each iteration."
            )
        return ChatMessage(content=x.content, role="assistant")

    def normalize_chunk(self, chunk: Any) -> ChatMessageChunk:
        x = cast("BaseMessageChunk", chunk)
        if isinstance(x.content, list):  # type: ignore
            raise ValueError(
                "The `message.content` provided seems to represent numerous messages. "
                "Consider iterating over `message.content` and calling .append_message() on each iteration."
            )
        return ChatMessageChunk(content=x.content, role="assistant")

    def can_normalize(self, message: Any) -> bool:
        try:
            from langchain_core.messages import BaseMessage

            return isinstance(message, BaseMessage)
        except Exception:
            return False

    def can_normalize_chunk(self, chunk: Any) -> bool:
        try:
            from langchain_core.messages import BaseMessageChunk

            return isinstance(chunk, BaseMessageChunk)
        except Exception:
            return False


class OpenAINormalizer(StringNormalizer):
    def normalize(self, message: Any) -> ChatMessage:
        x = cast("ChatCompletion", message)
        return super().normalize(x.choices[0].message.content)

    def normalize_chunk(self, chunk: Any) -> ChatMessageChunk:
        x = cast("ChatCompletionChunk", chunk)
        return super().normalize_chunk(x.choices[0].delta.content)

    def can_normalize(self, message: Any) -> bool:
        try:
            from openai.types.chat import ChatCompletion

            return isinstance(message, ChatCompletion)
        except Exception:
            return False

    def can_normalize_chunk(self, chunk: Any) -> bool:
        try:
            from openai.types.chat import ChatCompletionChunk

            return isinstance(chunk, ChatCompletionChunk)
        except Exception:
            return False


class AnthropicNormalizer(BaseMessageNormalizer):
    def normalize(self, message: Any) -> ChatMessage:
        x = cast("AnthropicMessage", message)
        content = x.content[0]
        if content.type != "text":
            raise ValueError(
                f"Anthropic message type {content.type} not supported. "
                "Only 'text' type is supported"
            )
        return ChatMessage(content=content.text, role="assistant")

    def normalize_chunk(self, chunk: Any) -> ChatMessageChunk:
        x = cast("MessageStreamEvent", chunk)
        content = ""
        if x.type == "content_block_delta":
            if x.delta.type != "text_delta":
                raise ValueError(
                    f"Anthropic message delta type {x.delta.type} not supported. "
                    "Only 'text_delta' type is supported"
                )
            content = x.delta.text

        type = "message_start" if x.type == "content_block_start" else "message_chunk"
        return ChatMessageChunk(content=content, type=type, role="assistant")

    def can_normalize(self, message: Any) -> bool:
        try:
            from anthropic.types import Message as AnthropicMessage

            return isinstance(message, AnthropicMessage)
        except Exception:
            return False

    def can_normalize_chunk(self, chunk: Any) -> bool:
        try:
            from anthropic.types import (
                RawContentBlockDeltaEvent,
                RawContentBlockStartEvent,
                RawContentBlockStopEvent,
                RawMessageDeltaEvent,
                RawMessageStartEvent,
                RawMessageStopEvent,
            )

            # The actual MessageStreamEvent is a generic, so isinstance() can't
            # be used to check the type. Instead, we manually construct the relevant
            # union of relevant classes...
            MessageStreamEvent = Union[
                RawMessageStartEvent,
                RawMessageDeltaEvent,
                RawMessageStopEvent,
                RawContentBlockStartEvent,
                RawContentBlockDeltaEvent,
                RawContentBlockStopEvent,
            ]

            return isinstance(chunk, MessageStreamEvent)
        except Exception:
            return False


class GoogleNormalizer(BaseMessageNormalizer):
    def normalize(self, message: Any) -> ChatMessage:
        msg = cast("GenerateContentResponse", message)
        return ChatMessage(content=msg.text, role="assistant")

    def normalize_chunk(self, chunk: Any) -> ChatMessageChunk:
        cnk = cast("GenerateContentResponse", chunk)
        return ChatMessageChunk(content=cnk.text, role="assistant")

    def can_normalize(self, message: Any) -> bool:
        try:
            from google.generativeai.types.generation_types import (  # pyright: ignore[reportMissingTypeStubs]
                GenerateContentResponse,
            )

            return isinstance(message, GenerateContentResponse)
        except Exception:
            return False

    def can_normalize_chunk(self, chunk: Any) -> bool:
        return self.can_normalize(chunk)


class OllamaNormalizer(DictNormalizer):
    def normalize(self, message: Any) -> ChatMessage:
        x = cast(dict[str, Any], message["message"])
        return super().normalize(x)

    def normalize_chunk(self, chunk: dict[str, Any]) -> ChatMessageChunk:
        msg = cast(dict[str, Any], chunk["message"])
        return super().normalize_chunk(msg)

    def can_normalize(self, message: Any) -> bool:
        if not isinstance(message, dict):
            return False
        if "message" not in message:
            return False
        return super().can_normalize(message["message"])

    def can_normalize_chunk(self, chunk: Any) -> bool:
        return self.can_normalize(chunk)


class NormalizerRegistry:
    def __init__(self) -> None:
        # Order of strategies matters (the 1st one that can normalize the message is used)
        # So make sure to put the most specific strategies first
        self._strategies: dict[str, BaseMessageNormalizer] = {
            "openai": OpenAINormalizer(),
            "anthropic": AnthropicNormalizer(),
            "google": GoogleNormalizer(),
            "langchain": LangChainNormalizer(),
            "ollama": OllamaNormalizer(),
            "dict": DictNormalizer(),
            "string": StringNormalizer(),
        }

    def register(
        self, provider: str, strategy: BaseMessageNormalizer, force: bool = False
    ) -> None:
        if provider in self._strategies and not force:
            raise ValueError(f"Provider {provider} already exists in registry")
        # Update the strategies dict such that the new strategy is the first to be considered
        strategies = {provider: strategy}
        strategies.update(self._strategies)


message_normalizer_registry = NormalizerRegistry()


def normalize_message(message: Any) -> ChatMessage:
    strategies = message_normalizer_registry._strategies
    for strategy in strategies.values():
        if strategy.can_normalize(message):
            return strategy.normalize(message)
    raise ValueError(
        f"Could not find a normalizer for message of type {type(message)}: {message}"
        "Consider registering a custom normalizer via shiny.ui._chat_types.registry.register()"
    )


def normalize_message_chunk(chunk: Any) -> ChatMessageChunk:
    strategies = message_normalizer_registry._strategies
    for strategy in strategies.values():
        if strategy.can_normalize_chunk(chunk):
            return strategy.normalize_chunk(chunk)
    raise ValueError(
        f"Could not find a normalizer for message chunk of type {type(chunk)}: {chunk}"
        "Consider registering a custom normalizer via shiny.ui._chat_types.registry.register()"
    )
