from __future__ import annotations

# Import these with underscore names so they won't show in autocomplete from the Python
# console.
from ..session import (
    Inputs as _Inputs,
    Outputs as _Outputs,
    Session as _Session,
    get_current_session as _get_current_session,
)
from .. import render
from . import ui
from ._is_express import is_express_app
from ._output import (  # noqa: F401
    output_args,  # pyright: ignore[reportUnusedImport]
    suspend_display,  # pyright: ignore[reportUnusedImport] - Deprecated
)
from ._run import wrap_express_app
from .expressify_decorator import expressify


__all__ = (
    "render",
    "input",
    "output",
    "session",
    "is_express_app",
    "wrap_express_app",
    "ui",
    "expressify",
)

# Add types to help type checkers
input: _Inputs
output: _Outputs
session: _Session


# Note that users should use `from shiny.express import input` instead of `from shiny
# import express` and acces via `express.input`. The former provides a static value for
# `input`, but the latter is dynamic -- every time `express.input` is accessed, it
# returns the input for the current session. This will work in the vast majority of
# cases, but when it fails, it will be very confusing.
def __getattr__(name: str) -> object:
    if name == "input":
        return _get_current_session().input  # pyright: ignore
    elif name == "output":
        return _get_current_session().output  # pyright: ignore
    elif name == "session":
        return _get_current_session()

    raise AttributeError(f"Module 'shiny.express' has no attribute '{name}'")
