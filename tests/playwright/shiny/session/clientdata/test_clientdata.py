import re

from playwright.sync_api import Page

from shiny.playwright import controller
from shiny.run import ShinyAppProc


def test_output_image_kitchen(page: Page, local_app: ShinyAppProc) -> None:

    page.goto(local_app.url)

    text = controller.OutputTextVerbatim(page, "clientdatatext")

    # This doesn't cover all the clientdata values since some of them
    # are environment-dependent. However, this at least checks that the
    # clientdata object is available and that some values are present.
    text.expect.to_contain_text("url_protocol = http")
    text.expect.to_contain_text("url_pathname = /")
    text.expect.to_contain_text(
        re.compile("url_hostname = (localhost|127\\.0\\.0\\.1)")
    )
    text.expect.to_contain_text("output_myplot_hidden = False")
    text.expect.to_contain_text("output_myplot_bg = rgb(255, 255, 255)")
    text.expect.to_contain_text("output_clientdatatext_hidden = False")
