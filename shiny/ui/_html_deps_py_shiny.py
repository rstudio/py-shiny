from __future__ import annotations

from htmltools import HTMLDependency, tags

from .. import __version__
from . import busy_indicators

"""
HTML dependencies for internal dependencies such as dataframe or text area's autoresize.

For...
* External dependencies (e.g. jQuery, Bootstrap), see `shiny.ui._html_deps_external`
* Internal dependencies (e.g. dataframe, autoresize), see `shiny.ui._html_deps_py_shiny`
* shinyverse dependencies (e.g. bslib, htmltools), see `shiny.ui._html_deps_shinyverse`
"""


def data_frame_deps() -> HTMLDependency:
    return HTMLDependency(
        name="shiny-data-frame-output",
        version=__version__,
        source={
            "package": "shiny",
            "subdir": "www/shared/py-shiny/data-frame",
        },
        script={"src": "data-frame.js", "type": "module"},
    )


def autoresize_dependency() -> HTMLDependency:
    return HTMLDependency(
        "shiny-textarea-autoresize",
        __version__,
        source={"package": "shiny", "subdir": "www/shared/py-shiny/text-area"},
        script={"src": "textarea-autoresize.js", "type": "module"},
        stylesheet={"href": "textarea-autoresize.css"},
    )


def page_output_dependency() -> HTMLDependency:
    return HTMLDependency(
        "shiny-page-output",
        __version__,
        source={"package": "shiny", "subdir": "www/shared/py-shiny/page-output"},
        script={"src": "page-output.js", "type": "module"},
    )


def spin_dependency() -> HTMLDependency:
    return HTMLDependency(
        "shiny-spin",
        __version__,
        source={"package": "shiny", "subdir": "www/shared/py-shiny/spin"},
        stylesheet={"href": "spin.css"},
    )


def busy_indicators_deps() -> list[HTMLDependency]:
    dep = HTMLDependency(
        "shiny-busy-indicators",
        __version__,
        source={"package": "shiny", "subdir": "www/shared/py-shiny/busy-indicators"},
        stylesheet={"href": "busy-indicators.css"},
        # Add a CSS class to the root element up until the next idle. The
        # busy-indicators.css above uses this class in order to indicate busy status
        # when the app is loading.
        # TODO: it'd be nice shiny.js did this
        head=tags.script(
            "document.documentElement.classList.add('shiny-not-yet-idle');"
            + "$(document).one('shiny:idle', function() { document.documentElement.classList.remove('shiny-not-yet-idle'); });"
        ),
    )

    return [
        dep,
        # Enable busy indicators by default.
        busy_indicators.use(),
    ]
