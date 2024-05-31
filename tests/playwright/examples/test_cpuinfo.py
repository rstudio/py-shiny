# pyright: reportUnknownMemberType=false

import re

from conftest import create_example_fixture

from shiny.test import Page, ShinyAppProc, expect

cpuinfo_app = create_example_fixture("cpuinfo")


def test_cpuinfo(page: Page, cpuinfo_app: ShinyAppProc):
    page.goto(cpuinfo_app.url)
    plot = page.locator("#plot")
    expect(plot).to_have_class(re.compile(r"\bshiny-bound-output\b"))
