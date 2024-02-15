from __future__ import annotations

import random
import warnings
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, Optional, cast, get_args

from htmltools import (
    HTML,
    Tag,
    TagAttrs,
    TagAttrValue,
    TagChild,
    TagList,
    css,
    div,
    tags,
)

from .._deprecated import warn_deprecated
from .._docstring import add_example, no_example
from .._namespaces import resolve_id_or_none
from ..session import require_active_session
from ._card import CardItem
from ._html_deps_shinyverse import components_dependency
from ._tag import consolidate_attrs, trinary
from ._utils import css_no_sub
from .css import CssUnit, as_css_padding, as_css_unit
from .fill import as_fill_item, as_fillable_container

if TYPE_CHECKING:
    from .. import Session

__all__ = (
    "Sidebar",
    "SidebarOpen",
    "sidebar",
    "layout_sidebar",
    "update_sidebar",
    # Legacy
    "panel_sidebar",
    "panel_main",
)

SidebarOpenValues = Literal["desktop", "open", "closed", "always"]
"""
The possible values for the `open` parameter in :func:`~shiny.ui.sidebar`.

* `"desktop"`: the sidebar starts open on desktop screen, closed on mobile
* `"open"`: the sidebar starts open
* `"closed"`: the sidebar starts closed
* `"always"`: the sidebar is always open and cannot be closed
"""


@dataclass
class SidebarOpen:
    """
    The initial state of the sidebar.

    TODO garrick-docs: Document this.
    """

    desktop: SidebarOpen._VALUES_TYPE = "open"
    mobile: SidebarOpen._VALUES_TYPE = "closed"

    _VALUES_TYPE = Literal["open", "closed", "always"]
    _VALUES: tuple[SidebarOpen._VALUES_TYPE, ...] = ("open", "closed", "always")

    @classmethod
    def _from_string(cls, open: str) -> SidebarOpen:
        if not isinstance(open, str) or len(open) == 0:
            raise ValueError("`open` must be a non-empty string")

        if open == "desktop":
            return cls(desktop="open", mobile="closed")
        elif open in cls._VALUES:
            return cls(desktop=open, mobile=open)
        else:
            raise ValueError(
                f"`open` must be one of {', '.join(cls._VALUES)}, or 'desktop'"
            )


@no_example()
class Sidebar:
    """
    A sidebar object

    Class returned from :func:`~shiny.ui.sidebar`. Please do not use this
    class directly. Instead, supply the :func:`~shiny.ui.sidebar` object to
    :func:`~shiny.ui.layout_sidebar`.

    TODO: garrick-docs: update after class restructuring

    Attributes
    ----------
    tag
        The :class:`~htmltools.Tag` object that represents the sidebar.
    collapse_tag
        The :class:`~htmltools.Tag` object that represents the collapse button.
    position
        Where the sidebar should appear relative to the main content.
    open
        The initial state of the sidebar (open or collapsed).
    width
        A valid CSS unit used for the width of the sidebar.
    max_height_mobile
        The maximum height of the horizontal sidebar when viewed on mobile devices.
        The default is `250px` unless the sidebar is included in a
        :func:`~shiny.ui.layout_sidebar` with a specified height, in
        which case the default is to take up no more than 50% of the layout container.
    color_fg
        A foreground color.
    color_bg
        A background color.

    Parameters
    ----------
    tag
        The :class:`~htmltools.Tag` object that represents the sidebar.
    collapse_tag
        The :class:`~htmltools.Tag` object that represents the collapse button.
    position
        Where the sidebar should appear relative to the main content.
    open
        The initial state of the sidebar (open or collapsed).
    width
        A valid CSS unit used for the width of the sidebar.
    max_height_mobile
        The maximum height of the horizontal sidebar when viewed on mobile devices.
        The default is `250px` unless the sidebar is included in a
        :func:`~shiny.ui.layout_sidebar` with a specified height, in
        which case the default is to take up no more than 50% of the layout container.
    color_fg
        A foreground color.
    color_bg
        A background color.
    """

    def __init__(
        self,
        children: tuple[TagChild | TagAttrs, ...],
        attributes: dict[str, TagAttrValue],
        width: CssUnit = 250,
        position: Literal["left", "right"] = "left",
        open: Optional[SidebarOpenValues | SidebarOpen] = None,
        id: Optional[str] = None,
        title: TagChild | str = None,
        color: dict[Literal["fg", "bg"], Optional[str]] = {},
        class_: Optional[str] = None,
        max_height_mobile: Optional[str | float] = None,
        gap: Optional[CssUnit] = None,
        padding: Optional[CssUnit | list[CssUnit]] = None,
    ):
        if isinstance(title, (str, int, float)):
            title = tags.header(str(title), class_="sidebar-title")

        if id is not None:
            if not isinstance(id, str):
                raise ValueError("`id` must be a single string")
            if isinstance(id, str) and len(id) == 0:
                raise ValueError("`id` must be a non-empty string")

        if open is not None and not isinstance(open, SidebarOpen):
            open = SidebarOpen._from_string(open)

        self.id = id
        self.title = title
        self.class_ = class_
        self.gap = as_css_unit(gap)
        self.padding = as_css_padding(padding)
        self._open = open
        self.position = position
        self.width = as_css_unit(width)
        self.max_height_mobile = max_height_mobile
        self.color = color
        self.attributes = attributes
        self.children = children

    @property
    def open(self) -> SidebarOpen:
        if isinstance(self._open, SidebarOpen):
            return self._open

        if self._open is None:
            return SidebarOpen()

        return SidebarOpen._from_string(self._open)

    def _resolved_sidebar_id(self) -> Optional[str]:
        if self.id is not None:
            return resolve_id_or_none(self.id)
        if not (self.open.desktop == "always" and self.open.mobile == "always"):
            return None

        # Provide a random id when sidebar is collapsible for accessibility reasons
        return f"bslib_sidebar_{random.randint(1000, 10000)}"

    def _collapse_tag(self) -> Tag:
        is_expanded = self.open.desktop == "open" or self.open.mobile == "open"

        return tags.button(
            _collapse_icon(),
            class_="collapse-toggle",
            type="button",
            title="Toggle sidebar",
            aria_expanded="true" if is_expanded else "false",
            aria_controls=resolve_id_or_none(self.id),
        )

    def _sidebar_tag(self) -> Tag:
        is_hidden_initially = (
            self.open.desktop == "closed" or self.open.mobile == "closed"
        )

        return tags.aside(
            {
                "id": self._resolved_sidebar_id(),
                "class": "sidebar",
                "hidden": "true" if is_hidden_initially else None,
            },
            # If the user provided an id, we make the sidebar an input to report state
            {"class": "bslib-sidebar-input"} if self.id is not None else None,
            div(
                {
                    "class": "sidebar-content bslib-gap-spacing",
                    "style": css(
                        gap=self.gap,
                        padding=self.padding,
                    ),
                },
                self.title,
                *self.children,
                **self.attributes,
            ),
            class_=self.class_,
        )

    def tagify(self) -> TagList:
        max_height_mobile = self.max_height_mobile

        if max_height_mobile is not None and self.open.mobile != "always":
            warnings.warn(
                "The `shiny.ui.sidebar(max_height_mobile=)` argument only applies to "
                + "the sidebar when `open` is `'always'` on mobile, but "
                + f"`open` is `'{self.open.mobile}'`. "
                + "The `max_height_mobile` argument will be ignored.",
                # `stacklevel=2`: Refers to the caller of `sidebar()`
                stacklevel=2,
            )
            max_height_mobile = None

        return TagList(
            self._sidebar_tag(),
            self._collapse_tag(),
        )


@add_example()
def sidebar(
    *args: TagChild | TagAttrs,
    width: CssUnit = 250,
    position: Literal["left", "right"] = "left",
    open: SidebarOpenValues | SidebarOpen = "desktop",
    id: Optional[str] = None,
    title: TagChild | str = None,
    bg: Optional[str] = None,
    fg: Optional[str] = None,
    class_: Optional[str] = None,
    max_height_mobile: Optional[str | float] = None,
    gap: Optional[CssUnit] = None,
    padding: Optional[CssUnit | list[CssUnit]] = None,
    **kwargs: TagAttrValue,
) -> Sidebar:
    # See [this article](https://rstudio.github.io/bslib/articles/sidebars.html)
    #   to learn more.
    # TODO-future; If color contrast is implemented. Docs for `bg` and `fg`:
    #     If only one of either is provided, an
    #     accessible contrasting color is provided for the opposite color, e.g. setting
    #     `bg` chooses an appropriate `fg` color.

    """
    Sidebar element

    Create a collapsing sidebar layout by providing a `sidebar()` object to the
    `sidebar=` argument of:

    * :func:`~shiny.ui.layout_sidebar`
      * Creates a sidebar layout component which can be dropped inside any Shiny UI page method (e.g. :func:`~shiny.ui.page_fillable`) or :func:`~shiny.ui.card` context.
    * :func:`~shiny.ui.navset_bar`, :func:`~shiny.ui.navset_card_tab`, and :func:`~shiny.ui.navset_card_pill`
      * Creates a multi page/tab UI with a singular `sidebar()` (which is
        shown on every page/tab).

    Parameters
    ----------
    *args
        Contents to the sidebar. Or tag attributes that are supplied to the
        resolved :class:`~htmltools.Tag` object.
    width
        A valid CSS unit used for the width of the sidebar.
    position
        Where the sidebar should appear relative to the main content.
    open
        The initial state of the sidebar.

        * `"desktop"`: the sidebar starts open on desktop screen, closed on mobile
        * `"open"` or `True`: the sidebar starts open
        * `"closed"` or `False`: the sidebar starts closed
        * `"always"` or `None`: the sidebar is always open and cannot be closed

        In :func:`~shiny.ui.update_sidebar`, `open` indicates the desired state of the
        sidebar. Note that :func:`~shiny.ui.update_sidebar` can only open or close the
        sidebar, so it does not support the `"desktop"` and `"always"` options.
    id
        A character string. Required if wanting to re-actively read (or update) the
        `collapsible` state in a Shiny app.
    title
        A character title to be used as the sidebar title, which will be wrapped in a
        `<div>` element with class `sidebar-title`. You can also provide a custom
        :class:`~htmltools.Tag` for the title element, in which case you'll
        likely want to give this element `class = "sidebar-title"`.
    bg,fg
        A background or foreground color.
    class_
        CSS classes for the sidebar container element, in addition to the fixed
        `.sidebar` class.
    max_height_mobile
        A CSS length unit (passed through :func:`~shiny.ui.css.as_css_unit`) defining
        the maximum height of the horizontal sidebar when viewed on mobile devices. Only
        applies to always-open sidebars that use `open = "always"`, where by default the
        sidebar container is placed below the main content container on mobile devices.
    gap
        A CSS length unit defining the vertical `gap` (i.e., spacing) between elements
        provided to `*args`.
    padding
        Padding within the sidebar itself. This can be a numeric vector (which will be
        interpreted as pixels) or a character vector with valid CSS lengths. `padding`
        may be one to four values.

        * If a single value, then that value will be used for all four sides.
        * If two, then the first value will be used for the top and bottom, while
          the second value will be used for left and right.
        * If three values, then the first will be used for top, the second will be left
          and right, and the third will be bottom.
        * If four, then the values will be interpreted as top, right, bottom, and left
          respectively.

    Returns
    -------
    :
        A :class:`~shiny.ui.Sidebar` object.

    See Also
    --------
    * :func:`~shiny.ui.layout_sidebar`
    * :func:`~shiny.ui.navset_bar`
    * :func:`~shiny.ui.navset_card_tab`
    * :func:`~shiny.ui.navset_card_pill`
    """
    # TODO-future; validate bg, fg, class_

    # TODO-future; implement
    # if fg is None and bg is not None:
    #     fg = get_color_contrast(bg)
    # if bg is None and fg is not None:
    #     bg = get_color_contrast(fg)

    return Sidebar(
        children=args,
        attributes=kwargs,
        width=width,
        position=position,
        open=open,
        id=id,
        title=title,
        color={"bg": bg, "fg": fg},
        class_=class_,
        max_height_mobile=max_height_mobile,
        gap=gap,
        padding=padding,
    )


@add_example()
def layout_sidebar(
    sidebar: Sidebar,
    *args: TagChild | TagAttrs,
    fillable: bool = True,
    fill: bool = True,
    bg: Optional[str] = None,
    fg: Optional[str] = None,
    border: Optional[bool] = None,
    border_radius: Optional[bool] = None,
    border_color: Optional[str] = None,
    gap: Optional[CssUnit] = None,
    padding: Optional[CssUnit | list[CssUnit]] = None,
    height: Optional[CssUnit] = None,
    **kwargs: TagAttrValue,
) -> CardItem:
    """
    Sidebar layout

    Create a sidebar layout component which can be dropped inside any Shiny UI page
    method (e.g. :func:`~shiny.ui.page_fillable`) or
    :func:`~shiny.ui.card` context.

    Parameters
    ----------
    *args
        One argument needs to be of class :class:`~shiny.ui.Sidebar` object created by
        :func:`~shiny.ui.sidebar`. The remaining arguments will contain the contents to
        the main content area. Or tag attributes that are supplied to the resolved
        :class:`~htmltools.Tag` object.
    fillable
        Whether or not the main content area should be wrapped in a fillable container.
        See :func:`~shiny.ui.fill.as_fillable_container` for details.
    fill
        Whether or not the sidebar layout should be wrapped in a fillable container. See
        :func:`~shiny.ui.fill.as_fill_item` for details.
    bg,fg
        A background or foreground color.
    border
        Whether or not to show a border around the sidebar layout.
    border_radius
        Whether or not to round the corners of the sidebar layout.
    border_color
        A border color.
    gap
        A CSS length unit defining the vertical `gap` (i.e., spacing) between elements
        provided to `*args`. This value will only be used if `fillable` is `True`.
    padding
        Padding within the sidebar itself. This can be a numeric vector (which will be
        interpreted as pixels) or a character vector with valid CSS lengths. `padding`
        may be one to four values.

        * If a single value, then that value will be used for all four sides.
        * If two, then the first value will be used for the top and bottom, while
          the second value will be used for left and right.
        * If three values, then the first will be used for top, the second will be left
          and right, and the third will be bottom.
        * If four, then the values will be interpreted as top, right, bottom, and left
          respectively.
    height
        Any valid CSS unit to use for the height.

    Returns
    -------
    :
        A :class:`~htmltools.Tag` object.

    See Also
    --------
    * :func:`~shiny.ui.sidebar`
    """

    sidebar, args = _get_layout_sidebar_sidebar(sidebar, args)

    # TODO-future; implement
    # if fg is None and bg is not None:
    #     fg = get_color_contrast(bg)
    # if bg is None and fg is not None:
    #     bg = get_color_contrast(fg)

    attrs, children = consolidate_attrs(*args, **kwargs)
    # TODO-future: >= 2023-11-01); Once `panel_main()` is removed, we can remove this loop
    for child in children:
        if isinstance(child, DeprecatedPanelMain):
            attrs = consolidate_attrs(attrs, child.attrs)[0]
            # child.children will be handled when tagified

    main = div(
        {
            "class": f"main{' bslib-gap-spacing' if fillable else ''}",
            "style": css(
                gap=as_css_unit(gap),
                padding=as_css_padding(padding),
            ),
        },
        attrs,
        *children,
    )
    if fillable:
        main = as_fillable_container(main)

    res = div(
        {"class": "bslib-sidebar-layout bslib-mb-spacing"},
        {"class": "sidebar-right"} if sidebar.position == "right" else None,
        {"class": "sidebar-collapsed"} if sidebar.open.desktop == "closed" else None,
        main,
        sidebar,
        components_dependency(),
        _sidebar_init_js(),
        data_bslib_sidebar_init="true",
        data_open_desktop=sidebar.open.desktop,
        data_open_mobile=sidebar.open.mobile,
        data_collapsible_mobile="true" if sidebar.open.mobile != "always" else "false",
        data_collapsible_desktop=(
            "true" if sidebar.open.desktop != "always" else "false"
        ),
        data_bslib_sidebar_border=trinary(border),
        data_bslib_sidebar_border_radius=trinary(border_radius),
        style=css_no_sub(
            **{
                "--_sidebar-width": sidebar.width,
                "--_sidebar-bg": sidebar.color["bg"],
                "--_sidebar-fg": sidebar.color["fg"],
                "--_main-fg": fg,
                "--_main-bg": bg,
                "--bs-card-border-color": border_color,
                "height": as_css_unit(height),
                "--_mobile-max-height": sidebar.max_height_mobile,
            },
        ),
    )
    if fill:
        res = as_fill_item(res)

    return CardItem(res)


def _get_layout_sidebar_sidebar(
    sidebar: Sidebar,
    args: tuple[TagChild | TagAttrs, ...],
) -> tuple[Sidebar, tuple[TagChild | TagAttrs, ...]]:
    updated_args: list[TagChild | TagAttrs] = []
    original_args = tuple(args)

    # sidebar: Sidebar | None = None
    sidebar_orig_arg: Sidebar | DeprecatedPanelSidebar = sidebar

    if isinstance(sidebar, DeprecatedPanelSidebar):
        sidebar = sidebar.sidebar

    if not isinstance(sidebar, Sidebar):
        raise ValueError(
            "`layout_sidebar()` is not being supplied with a `sidebar()` object. Please supply a `sidebar()` object to `layout_sidebar(sidebar)`."
        )

    # Use `original_args` here so `updated_args` can be safely altered in place
    for i, arg in zip(range(len(original_args)), original_args):
        if isinstance(arg, DeprecatedPanelSidebar):
            raise ValueError(
                "`panel_sidebar()` is not being used as the first argument to `layout_sidebar(sidebar,)`. `panel_sidebar()` has been deprecated and will go away in a future version of Shiny. Please supply `panel_sidebar()` arguments directly to `args` in `layout_sidebar(sidebar)` and use `sidebar()` instead of `panel_sidebar()`."
            )
        elif isinstance(arg, Sidebar):
            raise ValueError(
                "`layout_sidebar()` is being supplied with multiple `sidebar()` objects. Please supply only one `sidebar()` object to `layout_sidebar()`."
            )

        elif isinstance(arg, DeprecatedPanelMain):
            if i != 0:
                raise ValueError(
                    "`panel_main()` is not being supplied as the second argument to `layout_sidebar()`. `panel_main()`/`panel_sidebar()` have been deprecated and will go away in a future version of Shiny. Please supply `panel_main()` arguments directly to `args` in `layout_sidebar(sidebar, *args)` and use `sidebar()` instead of `panel_sidebar()`."
                )
            if not isinstance(sidebar_orig_arg, DeprecatedPanelSidebar):
                raise ValueError(
                    "`panel_main()` is not being used with `panel_sidebar()`. `panel_main()`/`panel_sidebar()` have been deprecated and will go away in a future version of Shiny. Please supply `panel_main()` arguments directly to `args` in `layout_sidebar(sidebar, *args)` and use `sidebar()` instead of `panel_sidebar()`."
                )

            if len(args) > 2:
                raise ValueError(
                    "Unexpected extra legacy `*args` have been supplied to `layout_sidebar()` in addition to `panel_main()` or `panel_sidebar()`. `panel_main()` has been deprecated and will go away in a future version of Shiny. Please supply `panel_main()` arguments directly to `args` in `layout_sidebar(sidebar, *args)` and use `sidebar()` instead of `panel_sidebar()`."
                )
            # Notes for this point in the code:
            # * We are working with args[0], a `DeprecatedPanelMain`; sidebar was originally a `DeprecatedPanelSidebar`
            # * len(args) == 1 or 2

            # Handle legacy `layout_sidebar(sidebar, main, position=)` value
            if len(args) == 2:
                arg1 = args[1]
                if not (arg1 == "left" or arg1 == "right"):
                    raise ValueError(
                        "layout_sidebar(*args) contains non-valid legacy values. Please use `sidebar()` instead of `panel_sidebar()` and supply any `panel_main()` arguments directly to `args` in `layout_sidebar(sidebar, *args)`."
                    )
                # We know `sidebar_orig_arg` is a `DeprecatedPanelSidebar` here
                sidebar.position = cast(  # pyright: ignore[reportOptionalMemberAccess]
                    Literal["left", "right"],
                    arg1,
                )

            # Only keep panel_main content
            updated_args = [arg]

            # Cases have been covered, quit loop
            break

            # Extract `DeprecatedPanelMain` attrs and children in followup for loop
        else:
            # Keep the arg!
            updated_args.append(arg)

    return (sidebar, tuple(updated_args))


@add_example()
def update_sidebar(
    id: str,
    *,
    show: Optional[bool] = None,
    session: Optional[Session] = None,
) -> None:
    """
    Update a sidebar's visibility.

    Set a :func:`~shiny.ui.sidebar` state during an active Shiny user session.

    Parameters
    ----------
    id
        The `id` of the :func:`~shiny.ui.sidebar` to toggle.
    show
        The desired visible state of the sidebar, where `True` opens the sidebar and `False` closes the sidebar (if not already in that state).
    session
        A Shiny session object (the default should almost always be used).

    See Also
    --------
    * :func:`~shiny.ui.sidebar`
    * :func:`~shiny.ui.layout_sidebar`
    """
    session = require_active_session(session)

    # method: Literal["toggle", "open", "close"]
    # if open is None or open == "toggle":
    #     method = "toggle"
    # elif open is True or open == "open":
    #     method = "open"
    # elif open is False or open == "closed":
    #     method = "close"
    # else:
    #     if open == "always" or open == "desktop":
    #         raise ValueError(
    #             f"`open = '{open}'` is not supported by `update_sidebar()`"
    #         )
    #     raise ValueError(
    #         "open must be NULL (or 'toggle'), TRUE (or 'open'), or FALSE (or 'closed')"
    #     )
    if show is not None:
        method = "open" if bool(show) else "close"

        def callback() -> None:
            session.send_input_message(id, {"method": method})

        session.on_flush(callback, once=True)


def _collapse_icon() -> TagChild:
    return HTML(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" class="bi bi-chevron-left collapse-icon" style="fill:currentColor;" aria-hidden="true" role="img" ><path fill-rule="evenodd" d="M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z"></path></svg>'
    )


def _sidebar_init_js() -> Tag:
    # Note: if we want to avoid inline `<script>` tags in the future for
    # initialization code, we might be able to do so by turning the sidebar layout
    # container into a web component
    return tags.script(
        {"data-bslib-sidebar-init": True},
        "bslib.Sidebar.initCollapsibleAll()",
    )


######################


# Deprecated 2023-06-13
# Includes: DeprecatedPanelSidebar
@no_example()
def panel_sidebar(
    *args: TagChild | TagAttrs,
    width: int = 4,
    **kwargs: TagAttrValue,
) -> DeprecatedPanelSidebar:
    """Deprecated. Please use :func:`~shiny.ui.sidebar` instead."""
    # TODO-future: >= 2024-01-01; Add deprecation message below
    # Plan of action:
    # * No deprecation messages today (2023-10-11), and existing code _just works_.
    # * Change all examples to use the new API.
    # * In, say, 6 months, start emitting messages for code that uses the old API.

    # warn_deprecated("Please use `sidebar()` instead of `panel_sidebar()`. `panel_sidebar()` will go away in a future version of Shiny.")
    return DeprecatedPanelSidebar(
        *args,
        width=width,
        **kwargs,
    )


# Deprecated 2023-06-13
# Includes: DeprecatedPanelMain
@no_example()
def panel_main(
    *args: TagChild | TagAttrs,
    width: int = 8,
    **kwargs: TagAttrValue,
) -> DeprecatedPanelMain:
    """Deprecated. Please supply the `*args` of :func:`~shiny.ui.panel_main` directly to :func:`~shiny.ui.layout_sidebar`."""
    # TODO-future: >= 2023-11-01; Add deprecation message below
    # warn_deprecated("Please use `layout_sidebar(*args)` instead of `panel_main()`. `panel_main()` will go away in a future version of Shiny.")

    # warn if keys are being ignored
    attrs, children = consolidate_attrs(*args, **kwargs)
    if len(attrs) > 0:
        return DeprecatedPanelMain(attrs=attrs, children=children)
        warn_deprecated(
            "`*args: TagAttrs` or `**kwargs: TagAttrValue` values supplied to `panel_main()` are being ignored. Please supply them directly to `layout_sidebar()`."
        )

    return DeprecatedPanelMain(attrs={}, children=children)


# Deprecated 2023-06-13


# This class should be removed when `panel_sidebar()` is removed
class DeprecatedPanelSidebar(
    # While it doesn't seem right to inherit from `Sidebar`, it's the easiest way to
    # make sure `layout_sidebar(sidebar: Sidebar)` works without mucking up the
    # function signature.
    Sidebar
):
    """
    [Deprecated] Sidebar panel

    Class returned from :func:`~shiny.ui.panel_sidebar`. Please do not
    use this class and instead supply your content to
    :func:`~shiny.ui.layout_sidebar` directly.

    Parameters
    ----------
    *args
        Contents to the sidebar. Or tag attributes that are supplied to the resolved
        :class:`~htmltools.Tag` object.
    width
        An integeger between 1 and 12, inclusive, that determines the width of the
        sidebar. The default is 4.
    **kwargs
        Tag attributes that are supplied to the resolved :class:`~htmltools.Tag` object.

    Attributes
    ----------
    sidebar
        A output from :func:`~shiny.ui.sidebar`.

    See Also
    --------
    * :func:`~shiny.ui.layout_sidebar`
    * :func:`~shiny.ui.sidebar`
    """

    # Store `attrs` for `layout_sidebar()` to retrieve
    sidebar: Sidebar

    def __init__(
        self, *args: TagChild | TagAttrs, width: int = 4, **kwargs: TagAttrValue
    ) -> None:
        self.sidebar = sidebar(
            *args,
            width=f"{int(width / 12 * 100)}%",
            open="always",
            **kwargs,  # pyright: ignore[reportArgumentType]
        )

    # Hopefully this is never used. But wanted to try to be safe
    def tagify(self) -> Tag:
        """
        Tagify the `self.sidebar.tag` and return the result in a TagList
        """
        return self.sidebar.tag.tagify()


# This class should be removed when `panel_main()` is removed
# Must be `Tagifiable`, so it can fit as a type `TagChild`
class DeprecatedPanelMain:
    """
    [Deprecated] Main panel

    Class returned from :func:`~shiny.ui.panel_main`. Please do not use
    this class and instead supply your content to
    :func:`~shiny.ui.layout_sidebar` directly.


    Parameters
    ----------
    attrs
        Attributes to apply to the parent tag of the children.
    children
        Children UI Elements to render inside the parent tag.

    Attributes
    ----------
    attrs
        Attributes to apply to the parent tag of the children.
    children
        Children UI Elements to render inside the parent tag.

    See Also
    --------
    * :func:`~shiny.ui.layout_sidebar`
    * :func:`~shiny.ui.sidebar`
    """

    # Store `attrs` for `layout_sidebar()` to retrieve
    attrs: TagAttrs
    # Return `children` in `layout_sidebar()` via `.tagify()` method
    children: list[TagChild]

    def __init__(self, *, attrs: TagAttrs, children: list[TagChild]) -> None:
        self.attrs = attrs
        self.children = children

    def tagify(self) -> TagList:
        """
        Tagify the `children` and return the result in a TagList
        """
        return TagList(self.children).tagify()
