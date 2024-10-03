from playwright.sync_api import Page

from shiny.playwright import controller
from shiny.run import ShinyAppProc


def test_sidebar_position_and_open(page: Page, local_app: ShinyAppProc) -> None:
    page.goto(local_app.url)

    left_sidebar = controller.Sidebar(page, "sidebar_left")
    output_txt_left = controller.OutputTextVerbatim(page, "state_left")
    left_sidebar.set(True)
    left_sidebar.expect_padding(["10px"])
    left_sidebar.expect_title("Left sidebar")
    left_sidebar.expect_gap("20px")
    left_sidebar.expect_class("text-white", has_class=True)
    left_sidebar.expect_bg_color("dodgerBlue")
    output_txt_left.expect_value("input.sidebar_left(): True")
    left_sidebar.expect_open(True)
    left_sidebar.set(False)
    output_txt_left.expect_value("input.sidebar_left(): False")
    left_sidebar.expect_handle(True)
    left_sidebar.expect_open(False)
    left_sidebar.loc_handle.click()
    left_sidebar.expect_open(True)
    output_txt_left.expect_value("input.sidebar_left(): True")

    right_sidebar = controller.Sidebar(page, "sidebar_right")
    right_sidebar.expect_padding(["10px", "20px"])
    right_sidebar.expect_bg_color("SlateBlue")

    closed_sidebar = controller.Sidebar(page, "sidebar_closed")
    closed_sidebar.expect_padding(["10px", "20px", "30px"])
    closed_sidebar.expect_bg_color("LightCoral")

    always_sidebar = controller.Sidebar(page, "sidebar_always")
    always_sidebar.expect_padding(["10px", "20px", "30px", "40px"])
    always_sidebar.expect_bg_color("PeachPuff")
