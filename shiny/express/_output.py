from __future__ import annotations

from contextlib import AbstractContextManager
from typing import Callable, TypeVar

from .._deprecated import warn_deprecated
from .._typing_extensions import ParamSpec
from ..render.renderer import RendererBaseT
from .ui import hold

__all__ = ("suspend_display",)

P = ParamSpec("P")
R = TypeVar("R")
CallableT = TypeVar("CallableT", bound=Callable[..., object])


# TODO-barret-future; quartodoc entry?
def output_args(
    **kwargs: object,
) -> Callable[[RendererBaseT], RendererBaseT]:
    """
    Sets default UI arguments for a Shiny rendering function.

    Each Shiny render function (like :func:`~shiny.render.plot`) can display itself when
    declared within a Shiny inline-style application. In the case of
    :func:`~shiny.render.plot`, the :func:`~shiny.ui.output_plot` function is called
    implicitly to display the plot. Use the `@ui_kwargs` decorator to specify arguments
    to be passed to `output_plot` (or whatever the corresponding UI function is) when
    the render function displays itself.

    Parameters
    ----------
    **kwargs
        Keyword arguments to be passed to the UI function.

    Returns
    -------
    :
        A decorator that sets the default UI arguments for a Shiny rendering function.
    """

    def wrapper(renderer: RendererBaseT) -> RendererBaseT:
        renderer._auto_output_ui_kwargs = kwargs
        return renderer

    return wrapper


def suspend_display(
    fn: Callable[P, R] | RendererBaseT | None = None
) -> Callable[P, R] | RendererBaseT | AbstractContextManager[None]:
    warn_deprecated(
        "`express.suspend_display()` is deprecated. Please use `express.ui.hold()` instead. "
        "It has a new name, but the exact same functionality."
    )
    return hold(fn)  # type: ignore
