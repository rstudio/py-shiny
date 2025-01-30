from playwright.sync_api import Page, expect

from shiny.run import ShinyAppProc


def is_element_scrolled_to_bottom(page: Page, selector: str) -> bool:
    return page.evaluate(
        """(selector) => {
        const element = document.querySelector(selector);
        if (!element) return false;

        // Get the exact scroll values (rounded to handle float values)
        const scrollTop = Math.round(element.scrollTop);
        const scrollHeight = Math.round(element.scrollHeight);
        const clientHeight = Math.round(element.clientHeight);

        // Check if the element is scrollable
        if (scrollHeight <= clientHeight) return false;

        // Check if we're at the bottom (allowing for 1px difference due to rounding)
        return Math.abs((scrollTop + clientHeight) - scrollHeight) <= 1;
    }""",
        selector,
    )


def test_validate_stream_basic(page: Page, local_app: ShinyAppProc) -> None:
    page.goto(local_app.url)

    stream = page.locator("#shiny-readme")
    expect(stream).to_be_visible(timeout=30 * 1000)
    expect(stream).to_contain_text("pip install shiny")

    # Check that the card body container (the parent of the markdown stream) is scrolled
    # all the way to the bottom
    is_scrolled = is_element_scrolled_to_bottom(page, ".card-body")
    assert is_scrolled, "The card body container should be scrolled to the bottom"
