from __future__ import annotations

import copy
from typing import Iterable, Literal

from htmltools import Tag, tags

from .._docstring import add_example, no_example

__all__ = ("use", "spinner_options")


BusyTypes = Literal["spinners", "pulse", "cursor"]


@add_example(ex_dir="../api-examples/busy_indicators")
def use(types: Iterable[BusyTypes] = ("spinners", "pulse")) -> Tag:
    """
    Use/customize busy indicators.

    Include the result of this function in the app's UI to use/customize busy indicators.
    Provide an empty list/tuple to disable all busy indicators.

    Parameters
    ----------
    types
        A list/tuple of busy indicator types, which can include:

        * `spinners`: Overlay a spinner on each recalculating output.
        * `pulse`: Show a pulsing banner at the top of the window when the server is busy.
        * `cursor`: Show a progress indicator on the mouse cursor whenever the server
           is busy. On mobile, a pulsing banner is shown instead.

    Returns
    -------
    :
        A `<style>` tag.

    See Also
    --------
    * :func:`~shiny.ui.busy_indicators.spinner_options`: Customize spinning busy indicators.
    """

    for x in types:
        if x not in ("spinners", "pulse", "cursor"):
            raise ValueError(f"Invalid busy indicator type: {x}")

    types_str = ",".join(types)

    return tags.script(
        f"$(function() {{ document.documentElement.dataset.shinyBusyIndicatorTypes = '{types_str}'; }});"
    )


@no_example()
def spinner_options(
    type: Literal["tadpole", "disc", "dots", "dot-track", "bounce"] | str | None = None,
    *,
    color: str | None = None,
    size: str | None = None,
    easing: str | None = None,
    speed: str | None = None,
    delay: str | None = None,
    css_selector: str = ":root",
) -> Tag:
    """
    Customize spinning busy indicators.

    Include the result of this function in the app's UI to customize spinner appearance.

    Parameters
    ----------
    type
        The type of spinner to use. Builtin options include: tadpole, disc, dots,
        dot-track, and bounce. A custom type may also provided, which should be a valid
        value for the CSS
        [mask-image](https://developer.mozilla.org/en-US/docs/Web/CSS/mask-image)
        property.
    color
        The color of the spinner. This can be any valid CSS color. Defaults to the
        app's "primary" color (if Bootstrap is on the page) or light-blue if not.
    size
        The size of the spinner. This can be any valid CSS size. Defaults to "40px".
    easing
        The easing function to use for the spinner animation. This can be any valid CSS
        [easing
        function](https://developer.mozilla.org/en-US/docs/Web/CSS/easing-function).
        Defaults to "linear".
    speed
        The amount of time for the spinner to complete a single revolution. This can be
        any valid CSS time. Defaults to "2s".
    delay
        The amount of time to wait before showing the spinner. This can be any valid CSS
        time. Defaults to "0.3s". This is useful for not showing the spinner if the
        computation finishes quickly.
    css_selector
        A CSS selector for scoping the spinner customization. Defaults to the root
        element.

    Returns
    -------
    :
        A `<style>` tag.
    """

    # bounce requires a different animation than the others
    if type == "bounce":
        animation = "shiny-busy-spinner-bounce"
        speed = speed or "0.8s"
    else:
        animation = None

    # Supported types have a CSS var already defined with their SVG data
    if type in ("tadpole", "disc", "dots", "dot-track", "bounce"):
        type = f"var(--_shiny-spinner-type-{type})"

    # Options are controlled via CSS variables.
    css_vars = (
        (f"--shiny-spinner-mask-img: {type};" if type else "")
        + (f"--shiny-spinner-easing: {easing};" if easing else "")
        + (f"--shiny-spinner-animation: {animation};" if animation else "")
        + (f"--shiny-spinner-color: {color};" if color else "")
        + (f"--shiny-spinner-size: {size};" if size else "")
        + (f"--shiny-spinner-speed: {speed};" if speed else "")
        + (f"--shiny-spinner-delay: {delay};" if delay else "")
    )

    # The CSS cascade allows this to be called multiple times, and as long as the CSS
    # selector is the same, the last call takes precedence. Also, css_selector allows
    # for scoping of the spinner customization.
    return tags.style(css_selector + " {" + css_vars + "}")
