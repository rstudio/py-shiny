# ------------------------------------------------------------------------------------
# When putting a Chat into production, there are at least a couple additional
# considerations to keep in mind:
#  - Token Limits: LLMs have (varying) limits on how many tokens can be included in
#    a single request and response. To accurately respect these limits, you'll want
#    to find the revelant limits and tokenizer for the model you're using, and inform
#    Chat about them.
#  - Reproducibility: Consider pinning a snapshot of the LLM model to ensure that the
#    same model is used each time the app is run.
#
# See the MODEL_INFO dictionary below for an example of how to set these values for
# Anthropic's Claude model.
# https://docs.anthropic.com/en/docs/about-claude/models#model-comparison-table
# ------------------------------------------------------------------------------------
import os

from anthropic import AsyncAnthropic
from app_utils import load_dotenv

from shiny.express import ui

load_dotenv()
llm = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


MODEL_INFO = {
    "name": "claude-3-sonnet-20240229",
    # DISCLAIMER: Anthropic has not yet released a public tokenizer for Claude models,
    # so this uses the generic default provided by Chat() (for now). That is probably
    # ok though since the default tokenzier likely overestimates the token count.
    "tokenizer": None,
    "token_limits": (200000, 4096),
}


ui.page_opts(
    title="Hello OpenAI Chat",
    fillable=True,
    fillable_mobile=True,
)

chat = ui.Chat(
    id="chat",
    messages=[
        {"content": "Hello! How can I help you today?", "role": "assistant"},
    ],
    tokenizer=MODEL_INFO["tokenizer"],
)

chat.ui()


@chat.on_user_submit
async def _():
    messages = chat.messages(format="openai", token_limits=MODEL_INFO["token_limits"])
    response = await llm.chat.completions.create(
        model=MODEL_INFO["name"], messages=messages, stream=True
    )
    await chat.append_message_stream(response)
