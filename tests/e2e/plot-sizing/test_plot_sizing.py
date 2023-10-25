import re

from conftest import ShinyAppProc
from controls import OutputPlot
from playwright.sync_api import Page


def test_output_image_kitchen(page: Page, local_app: ShinyAppProc) -> None:
    page.goto(local_app.url)

    plotids_by_tab = {
        "mpl": [
            "mpl-plot_default",
            "mpl-plot_dom_size",
            "mpl-plot_decorator_size",
            "mpl-plot_native_size",
        ],
        "plotnine": [
            "plotnine-plot_default",
            "plotnine-plot_dom_size",
            "plotnine-plot_decorator_size",
            "plotnine-plot_native_size",
        ],
        "pil": [
            "pil-plot_default",
            "pil-plot_dom_size",
            "pil-plot_decorator_size",
        ],
    }

    for tab, plots in plotids_by_tab.items():
        page.click(f"a[data-toggle='tab'][data-value='{tab}']")
        for plotid in plots:
            img = OutputPlot(page, plotid)
            # These assertions are mostly to ensure that the plots load before we
            # evaluate their sizes
            img.expect_inline(inline=False)
            img.expect_img_src(re.compile(r"data:image/png;base64"), timeout=20)

            rect = page.evaluate(
                f"() => document.querySelector('#{plotid} img').getBoundingClientRect()"
            )
            assert rect["width"] == 300
            assert rect["height"] == 200
