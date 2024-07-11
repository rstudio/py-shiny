import sys
from typing import TYPE_CHECKING, Literal, TypedDict

from ._chat_types import ChatMessage

if TYPE_CHECKING:
    from anthropic.types import MessageParam as AnthropicMessage
    from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
    from ollama import Message as OllamaMessage
    from openai.types.chat import (
        ChatCompletionAssistantMessageParam,
        ChatCompletionSystemMessageParam,
        ChatCompletionUserMessageParam,
    )

    if sys.version_info >= (3, 9):
        from google.generativeai.types import ContentDict as GoogleMessage
    else:

        class GoogleMessage(TypedDict):
            parts: list[str]
            role: str

    LangChainMessage = AIMessage | HumanMessage | SystemMessage
    OpenAIMessage = (
        ChatCompletionAssistantMessageParam
        | ChatCompletionSystemMessageParam
        | ChatCompletionUserMessageParam
    )

    ProviderMessage = (
        AnthropicMessage
        | GoogleMessage
        | LangChainMessage
        | OpenAIMessage
        | OllamaMessage
    )
else:
    AnthropicMessage = GoogleMessage = LangChainMessage = OpenAIMessage = (
        OllamaMessage
    ) = ProviderMessage = object

ProviderMessageFormat = Literal[
    "anthropic",
    "google",
    "langchain",
    "openai",
    "ollama",
]


def as_provider_message(
    message: ChatMessage, format: ProviderMessageFormat
) -> "ProviderMessage":
    if format == "anthropic":
        return as_anthropic_message(message)
    if format == "google":
        return as_google_message(message)
    if format == "langchain":
        return as_langchain_message(message)
    if format == "openai":
        return as_openai_message(message)
    if format == "ollama":
        return as_ollama_message(message)
    raise ValueError(f"Unknown format: {format}")


def as_anthropic_message(message: ChatMessage) -> "AnthropicMessage":
    from anthropic.types import MessageParam as AnthropicMessage

    if message["role"] == "system":
        raise ValueError(
            "Anthropic requires a system prompt to be specified in the `.create()` method"
        )
    return AnthropicMessage(content=message["content"], role=message["role"])


def as_google_message(message: ChatMessage) -> "GoogleMessage":
    from google.generativeai.types import ContentDict as GoogleMessage

    if message["role"] == "system":
        raise ValueError(
            "Google requires a system prompt to be specified in the `GenerativeModel()` constructor."
        )
    return GoogleMessage(parts=[message["content"]], role=message["role"])


def as_langchain_message(message: ChatMessage) -> "LangChainMessage":
    from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

    content = message["content"]
    role = message["role"]
    if role == "system":
        return SystemMessage(content=content)
    if role == "assistant":
        return AIMessage(content=content)
    if role == "user":
        return HumanMessage(content=content)
    raise ValueError(f"Unknown role: {message['role']}")


def as_openai_message(message: ChatMessage) -> "OpenAIMessage":
    from openai.types.chat import (
        ChatCompletionAssistantMessageParam,
        ChatCompletionSystemMessageParam,
        ChatCompletionUserMessageParam,
    )

    content = message["content"]
    role = message["role"]
    if role == "system":
        return ChatCompletionSystemMessageParam(content=content, role=role)
    if role == "assistant":
        return ChatCompletionAssistantMessageParam(content=content, role=role)
    if role == "user":
        return ChatCompletionUserMessageParam(content=content, role=role)
    raise ValueError(f"Unknown role: {role}")


def as_ollama_message(message: ChatMessage) -> "OllamaMessage":
    from ollama import Message as OllamaMessage

    return OllamaMessage(content=message["content"], role=message["role"])
