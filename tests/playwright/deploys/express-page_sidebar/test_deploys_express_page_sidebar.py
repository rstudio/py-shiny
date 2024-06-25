import pytest
from playwright.sync_api import Page
from utils.deploy_utils import (
    create_deploys_app_url_fixture,
    reruns,
    reruns_delay,
    skip_if_not_chrome,
)

from shiny.playwright import controller

app_url = create_deploys_app_url_fixture("express_page_sidebar")


@skip_if_not_chrome
@pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
def test_express_page_sidebar(page: Page, app_url: str) -> None:
    page.goto(app_url)

    sidebar = controller.Sidebar(page, "sidebar")
    sidebar.expect_text("SidebarTitle Sidebar Content")
    output_txt = controller.OutputTextVerbatim(page, "txt")
    output_txt.expect_value("50")
