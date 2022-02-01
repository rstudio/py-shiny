__all__ = ("insert_ui", "remove_ui")

import sys
from typing import Optional

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

from htmltools import TagChildArg

from .._docstring import doc
from ..session import Session, require_active_session

_common_params = {
    "multiple": """
    In case your selector matches more than one element, multiple determines whether
    Shiny should insert the UI object relative to all matched elements or just relative
    to the first matched element (default).
    """,
    "immediate": """
    Whether the UI object should be immediately inserted or removed, or whether Shiny
    should wait until all outputs have been updated and all effects have been run
    (default).
    """,
}

_insert_params = {
    "ui": """
    The UI object you want to insert. This can be anything that you usually put inside
    your apps's ui function. If you're inserting multiple elements in one call, make
    sure to wrap them in either a :func:`~shiny.ui.tagList()` or a
    :func:`~shiny.ui.tags.div()` (the latter option has the advantage that you can give
    it an id to make it easier to reference or remove it later on). If you want to
    insert raw html, use :func:`~shiny.ui.HTML()`.
    """,
    "selector": """
    A string that is accepted by jQuery's selector (i.e. the string ``s`` to be placed
    in a ``$(s)`` jQuery call) which determines the element(s) relative
    to which you want to insert your UI object.
    """,
    "where": """
Where your UI object should go relative to the selector:

* beforeBegin: Before the selector element itself

* afterBegin: Just inside the selector element, before its first child

* beforeEnd: Just inside the selector element, after its last child (default)

* afterEnd: After the selector element itself

Adapted from https://developer.mozilla.org/en-US/docs/Web/API/Element/insertAdjacentHTML.
""",
}


@doc(
    "Insert UI objects",
    parameters={**_common_params, **_insert_params},
    note="""
    This function allows you to dynamically add arbitrary UI into your app, whenever you
    want, as many times as you want. Unlike :func:`shiny.render_ui`, the UI generated
    with `insert_ui` is persistent: once it's created, it stays there until removed by
    :func:`remove_ui`. Each new call to `insert_ui` creates more UI objects, in addition
    to the ones already there (all independent from one another). To update a part of
    the UI (ex: an input object), you must use the appropriate render function or a
    customized reactive function.
    """,
    see_also=[
        ":func:`~shiny.ui.remove_ui`",
        ":func:`~shiny.render_ui`",
    ],
)
def insert_ui(
    ui: TagChildArg,
    selector: str,
    where: Literal["beforeBegin", "afterBegin", "beforeEnd", "afterEnd"] = "beforeEnd",
    multiple: bool = False,
    immediate: bool = False,
    session: Optional[Session] = None,
) -> None:

    session = require_active_session(session)

    def callback() -> None:
        session.send_insert_ui(
            selector=selector,
            multiple=multiple,
            where=where,
            content=session.process_ui(ui),
        )

    if immediate:
        callback()
    else:
        session.on_flushed(callback, once=True)


_remove_params = {
    "selector": """
    A string that is accepted by jQuery's selector (i.e. the string ``x`` to be placed
    in a ``$(x)`` jQuery call) which determines the element(s) to remove. If you want to
    remove a Shiny input or output, note that many of these are wrapped in ``<div>``s,
    so you may need to use a somewhat complex selector — see the Examples below.
    (Alternatively, you could also wrap the inputs/outputs that you want to be able to
    remove easily in a ``<div>`` with an id.)
    """,
}


@doc(
    "Remove UI objects",
    parameters={**_common_params, **_remove_params},
    see_also=[
        ":func:`~shiny.ui.insert_ui`",
        ":func:`~shiny.render_ui`",
    ],
)
def remove_ui(
    selector: str,
    multiple: bool = False,
    immediate: bool = False,
    session: Optional[Session] = None,
) -> None:

    session = require_active_session(session)

    def callback():
        session.send_remove_ui(selector=selector, multiple=multiple)

    if immediate:
        callback()
    else:
        session.on_flushed(callback, once=True)
