from conftest import ShinyAppProc, x_create_doc_example_fixture
from controls import Card
from playwright.sync_api import Page

app = x_create_doc_example_fixture("card")


def test_card(page: Page, app: ShinyAppProc) -> None:
    page.goto(app.url)

    card = Card(page, "card1")
    card.expect_max_height(None)
    card.expect_min_height(None)
    card.expect_height(None)
    card.expect_header_to_contain_text("This is the header")
    card.expect_footer_to_contain_text("This is the footer")
    card.expect_body_to_contain_text(
        [
            "\nThis is the title\nThis is the body.\n",
            "\n\n",
            "\nThis is still the body.\n",
        ]
    )
    card.expect_full_screen(False)
    card.open_full_screen()
    card.expect_full_screen(True)
    card.close_full_screen()
    card.expect_full_screen(False)
