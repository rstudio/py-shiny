import time

import requests

from shiny.express import session, ui

# Read in the README.md file from the py-shiny repository
response = requests.get(
    "https://raw.githubusercontent.com/posit-dev/py-shiny/refs/heads/main/README.md"
)
content = response.text.replace("\n", " \n ")


# Generate words from the README.md file (with a small delay)
def generate_words():
    for word in content.split(" "):
        if not session.is_stub_session():
            time.sleep(0.05)
        yield word + " "


md = ui.MarkdownStream("shiny-readme")
md.ui()
md.stream(generate_words())
