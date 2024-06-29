from typing import Union

from shiny.express import render, ui

# Set some Shiny page options
ui.page_opts(title="Hello Chat")

# Create a chat instance, with an initial message
chat = ui.Chat(id="chat")

# Display the chat
chat.ui()


@chat.transform_user_input
async def capitalize(input: str) -> Union[str, None]:
    if input == "return None":
        return None
    elif input == "return custom message":
        await chat.append_message("Custom message")
        return None
    else:
        return input.upper()


@chat.on_user_submit
async def _():
    user = chat.get_user_input(transform=True)
    await chat.append_message(f"Transformed input: {user}")


"Message state:"


@render.code
def message_state():
    return str(chat.get_messages())
