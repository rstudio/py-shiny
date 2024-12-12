# ------------------------------------------------------------------------------------
# A basic Shiny Chat example powered by Ollama.
# ------------------------------------------------------------------------------------

from chatlas import ChatOllama

from shiny.express import ui

# ChatOllama() requires an Ollama model server to be running locally.
# See the docs for more information on how to set up a local Ollama server.
# https://posit-dev.github.io/chatlas/reference/ChatOllama.html
chat_model = ChatOllama(model="llama3.1")

# Set some Shiny page options
ui.page_opts(
    title="Hello Ollama Chat",
    fillable=True,
    fillable_mobile=True,
)

# Create and display a Shiny chat component
chat = ui.Chat(
    id="chat",
    messages=["Hello! How can I help you today?"],
)
chat.ui()


# Generate a response when the user submits a message
@chat.on_user_submit
async def _(message):
    response = chat_model.stream(message)
    await chat.append_message_stream(response)
