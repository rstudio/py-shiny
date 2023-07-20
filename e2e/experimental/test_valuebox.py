import pytest
from conftest import ShinyAppProc, x_create_doc_example_fixture
from controls import ValueBox
from playwright.sync_api import Page

app = x_create_doc_example_fixture("value_box")


@pytest.mark.parametrize("value_box_id", ["valuebox1", "valuebox2"])
def test_valuebox(page: Page, app: ShinyAppProc, value_box_id: str) -> None:
    page.goto(app.url)

    value_box = ValueBox(page, value_box_id)
    value_box.expect_height(None)
    value_box.expect_title("KPI Title")
    value_box.expect_full_screen(False)
    value_box.open_full_screen()
    value_box.expect_full_screen(True)
    value_box.expect_body(
        ["$1 Billion Dollars", "30% VS PREVIOUS 30 DAYS"]
    )
    value_box.close_full_screen()
    value_box.expect_full_screen(False)
