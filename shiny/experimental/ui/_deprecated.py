from __future__ import annotations

from typing import Any, Literal, Optional, TypeVar, overload

from htmltools import Tag, TagAttrs, TagAttrValue, TagChild, TagFunction, TagList

from ..._deprecated import warn_deprecated
from ...session import Session
from ...ui import input_text_area as main_input_text_area
from ...ui import popover as main_popover
from ...ui import tags
from ...ui import toggle_popover as main_toggle_popover
from ...ui import toggle_switch as main_toggle_switch
from ...ui import toggle_tooltip as main_toggle_tooltip
from ...ui import tooltip as main_tooltip
from ...ui import update_popover as main_update_popover
from ...ui import update_tooltip as main_update_tooltip

# from ...ui import AccordionPanel as MainAccordionPanel
# from ...ui import accordion as main_accordion
# from ...ui import accordion_panel as main_accordion_panel
# from ...ui import accordion_panel_close as main_accordion_panel_close
# from ...ui import accordion_panel_insert as main_accordion_panel_insert
# from ...ui import accordion_panel_open as main_accordion_panel_open
# from ...ui import accordion_panel_remove as main_accordion_panel_remove
# from ...ui import accordion_panel_set as main_accordion_panel_set
# from ...ui import update_accordion_panel as main_update_accordion_panel
from ...ui._card import CardItem as MainCardItem
from ...ui._card import WrapperCallable as MainWrapperCallable
from ...ui._card import card_footer as main_card_footer
from ...ui._card import card_header as main_card_header
from ...ui._layout import layout_column_wrap as main_layout_column_wrap
from ...ui._tag import consolidate_attrs
from ...ui.css_unit._css_unit import CssUnit as MainCssUnit
from ...ui.css_unit._css_unit import as_css_padding as main_as_css_padding
from ...ui.css_unit._css_unit import as_css_unit as main_as_css_unit
from ...ui.css_unit._css_unit import as_width_unit as main_as_width_unit
from ...ui.fill import as_fill_carrier as main_as_fill_carrier
from ...ui.fill import as_fill_item as main_as_fill_item
from ...ui.fill import as_fillable_container as main_as_fillable_container
from ...ui.fill import is_fill_carrier as main_is_fill_carrier
from ...ui.fill import is_fill_item as main_is_fill_item
from ...ui.fill import is_fillable_container as main_is_fillable_container
from ...ui.fill import remove_all_fill as main_remove_all_fill
from ._navs import NavSetArg, NavSetCard, navset_card_pill, navset_card_tab
from ._sidebar import (
    DeprecatedPanelMain,
    DeprecatedPanelSidebar,
    Sidebar,
    toggle_sidebar,
)

# from ...types import MISSING, MISSING_TYPE


__all__ = (
    # Input Switch
    "toggle_switch",
    # Input Text Area
    "input_text_area",
    # Navs
    "navset_pill_card",
    "navset_tab_card",
    # Tooltip
    "tooltip_update",
    "tooltip_toggle",
    "tooltip",
    "toggle_tooltip",
    "update_tooltip",
    # Sidebar
    "sidebar_toggle",
    "panel_sidebar",
    "panel_main",
    "DeprecatedPanelSidebar",
    "DeprecatedPanelMain",
    # Css Unit
    "CssUnit",
    "as_css_unit",
    "as_css_padding",
    "as_width_unit",
    # Popover
    "popover",
    "toggle_popover",
    "update_popover",
    # # Accordion
    # "AccordionPanel",
    # "accordion",
    # "accordion_panel",
    # "accordion_panel_set",
    # "accordion_panel_open",
    # "accordion_panel_close",
    # "accordion_panel_insert",
    # "accordion_panel_remove",
    # "update_accordion_panel",
    # Fill
    "as_fill_carrier",
    "as_fillable_container",
    "as_fill_item",
    "remove_all_fill",
    "is_fill_carrier",
    "is_fillable_container",
    "is_fill_item",
    # Card
    "TagCallable",
    "CardItem",
    "card_header",
    "card_footer",
)

######################
# Input Switch
######################


# Deprecated 2023-09-12
def toggle_switch(
    id: str,
    value: Optional[bool] = None,
    session: Optional[Session] = None,
) -> None:
    """Deprecated. Please use `shiny.ui.toggle_switch()` instead."""
    warn_deprecated(
        "`shiny.experimental.ui.toggle_switch()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.ui.toggle_switch` instead."
    )
    return main_toggle_switch(id, value, session=session)


######################
# Input Text Area
######################


# Deprecated 2023-09-12
def input_text_area(
    id: str,
    label: TagChild,
    value: str = "",
    *,
    width: Optional[str] = None,
    height: Optional[str] = None,
    cols: Optional[int] = None,
    rows: Optional[int] = None,
    placeholder: Optional[str] = None,
    resize: Optional[Literal["none", "both", "horizontal", "vertical"]] = None,
    autoresize: bool = False,
    autocomplete: Optional[str] = None,
    spellcheck: Optional[Literal["true", "false"]] = None,
) -> Tag:
    """Deprecated. Please use `shiny.ui.input_text_area()` instead."""
    warn_deprecated(
        "`shiny.experimental.ui.input_text_area()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.ui.input_text_area` instead."
    )
    return main_input_text_area(
        id,
        label,
        value=value,
        width=width,
        height=height,
        cols=cols,
        rows=rows,
        placeholder=placeholder,
        resize=resize,
        autoresize=autoresize,
        autocomplete=autocomplete,
        spellcheck=spellcheck,
    )


######################
# Navs
######################


# Deprecated 2023-08-15
def navset_pill_card(
    *args: NavSetArg,
    id: Optional[str] = None,
    selected: Optional[str] = None,
    sidebar: Optional[Sidebar] = None,
    header: TagChild = None,
    footer: TagChild = None,
    placement: Literal["above", "below"] = "above",
) -> NavSetCard:
    """Deprecated. Please use `navset_card_pill()` instead of `navset_pill_card()`."""
    warn_deprecated(
        "`navset_pill_card()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.experimental.ui.navset_card_pill` instead."
    )
    return navset_card_pill(
        *args,
        id=id,
        selected=selected,
        sidebar=sidebar,
        header=header,
        footer=footer,
        placement=placement,
    )


# Deprecated 2023-08-15
def navset_tab_card(
    *args: NavSetArg,
    id: Optional[str] = None,
    selected: Optional[str] = None,
    sidebar: Optional[Sidebar] = None,
    header: TagChild = None,
    footer: TagChild = None,
) -> NavSetCard:
    """Deprecated. Please use `navset_card_tab()` instead of `navset_tab_card()`."""
    warn_deprecated(
        "`navset_tab_card()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.experimental.ui.navset_card_tab` instead."
    )
    return navset_card_tab(
        *args,
        id=id,
        selected=selected,
        header=header,
        footer=footer,
    )


######################
# Tooltip
######################


# Deprecated 2023-09-12
def tooltip(
    trigger: TagChild,
    *args: TagChild | TagAttrs,
    id: Optional[str] = None,
    placement: Literal["auto", "top", "right", "bottom", "left"] = "auto",
    options: Optional[dict[str, object]] = None,
    **kwargs: TagAttrValue,
) -> Tag:
    """Deprecated. Please use `shiny.ui.tooltip()` instead."""
    warn_deprecated(
        "`shiny.experimental.ui.tooltip()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.ui.tooltip` instead."
    )
    return main_tooltip(
        trigger,
        *args,
        id=id,
        placement=placement,
        options=options,
        **kwargs,
    )


# Deprecated 2023-08-23
def tooltip_update(id: str, *args: TagChild, session: Optional[Session] = None) -> None:
    """Deprecated. Please use `shiny.ui.update_tooltip()` instead."""
    warn_deprecated(
        "`shiny.experimental.ui.tooltip_update()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.ui.update_tooltip` instead."
    )
    main_update_tooltip(
        id,
        *args,
        session=session,
    )


# Deprecated 2023-09-12
def update_tooltip(id: str, *args: TagChild, session: Optional[Session] = None) -> None:
    """Deprecated. Please use `shiny.ui.update_tooltip()` instead."""
    warn_deprecated(
        "`shiny.experimental.ui.update_tooltip()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.ui.update_tooltip` instead."
    )
    main_update_tooltip(
        id,
        *args,
        session=session,
    )


# Deprecated 2023-08-23
def tooltip_toggle(
    id: str,
    show: Optional[bool] = None,
    session: Optional[Session] = None,
) -> None:
    """Deprecated. Please use `shiny.ui.toggle_tooltip()`."""
    warn_deprecated(
        "`shiny.experimental.ui.tooltip_toggle()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.ui.toggle_tooltip` instead."
    )
    main_toggle_tooltip(
        id=id,
        show=show,
        session=session,
    )


# Deprecated 2023-09-12
def toggle_tooltip(
    id: str,
    show: Optional[bool] = None,
    session: Optional[Session] = None,
) -> None:
    """Deprecated. Please use `shiny.ui.toggle_tooltip()` instead."""
    warn_deprecated(
        "`shiny.experimental.ui.tooltip_toggle()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.ui.toggle_tooltip` instead."
    )
    main_toggle_tooltip(
        id=id,
        show=show,
        session=session,
    )


######################
# Sidebar
######################


# Deprecated 2023-08-23
def sidebar_toggle(
    id: str,
    open: Literal["toggle", "open", "closed", "always"] | bool | None = None,
    session: Session | None = None,
) -> None:
    """Deprecated. Please use `toggle_sidebar()` instead of `sidebar_toggle()`."""
    warn_deprecated(
        "`sidebar_toggle()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.experimental.ui.toggle_sidebar` instead."
    )
    toggle_sidebar(
        id=id,
        open=open,
        session=session,
    )


# Deprecated 2023-06-13
# Includes: DeprecatedPanelSidebar
def panel_sidebar(
    *args: TagChild | TagAttrs,
    width: int = 4,
    **kwargs: TagAttrValue,
) -> DeprecatedPanelSidebar:
    """Deprecated. Please use :func:`shiny.experimental.ui.sidebar` instead of
    `ui.panel_sidebar()`."""
    # TODO-future: >= 2023-11-01; Add deprecation message below
    # Plan of action:
    # * No deprecation messages today (2023-05-18), and existing code _just works_.
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
def panel_main(
    *args: TagChild | TagAttrs,
    width: int = 8,
    **kwargs: TagAttrValue,
) -> TagList | DeprecatedPanelMain:
    """Deprecated. Please supply `panel_main(*args)` directly to `layout_sidebar()`."""
    # TODO-future: >= 2023-11-01; Add deprecation message below
    # warn_deprecated(
    #     "Please supply `panel_main(*args)` directly to `layout_sidebar()`."
    # )
    # warn if keys are being ignored
    attrs, children = consolidate_attrs(*args, **kwargs)
    if len(attrs) > 0:
        return DeprecatedPanelMain(attrs=attrs, children=children)
        warn_deprecated(
            "`*args: TagAttrs` or `**kwargs: TagAttrValue` values supplied to `panel_main()` are being ignored. Please supply them directly to `layout_sidebar()`."
        )

    return TagList(*children)


######################
# Css Unit
######################

# Deprecated 2023-09-12
CssUnit = MainCssUnit
"""
Deprecated. Please use `shiny.ui.css_unit.CssUnit` instead.
"""


@overload
def as_css_unit(value: None) -> None:
    ...


@overload
def as_css_unit(value: CssUnit) -> str:
    ...


# Deprecated 2023-09-12
def as_css_unit(value: None | CssUnit) -> None | str:
    """
    Deprecated. Please use `shiny.ui.css_unit.as_css_unit()` instead.
    """
    warn_deprecated(
        "`shiny.experimental.ui.as_css_unit()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.ui.css_unit.as_css_unit` instead."
    )
    return main_as_css_unit(value)


@overload
def as_css_padding(padding: CssUnit | list[CssUnit]) -> str:
    ...


@overload
def as_css_padding(padding: None) -> None:
    ...


# Deprecated 2023-09-12
def as_css_padding(padding: CssUnit | list[CssUnit] | None) -> str | None:
    """
    Deprecated. Please use `shiny.ui.css_unit.as_css_padding()` instead.
    """
    warn_deprecated(
        "`shiny.experimental.ui.as_css_padding()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.ui.css_unit.as_css_padding` instead."
    )
    return main_as_css_padding(padding)


# Deprecated 2023-09-12
def as_width_unit(x: str | float | int) -> str:
    """Deprecated. Please use `shiny.ui.css_unit.as_width_unit()` instead."""
    warn_deprecated(
        "`shiny.experimental.ui.as_width_unit()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.ui.css_unit.as_width_unit` instead."
    )
    return main_as_width_unit(x)


######################
# Popover
######################


# Deprecated 2023-09-12
def popover(
    trigger: TagChild,
    *args: TagChild | TagAttrs,
    title: Optional[TagChild] = None,
    id: Optional[str] = None,
    placement: Literal["auto", "top", "right", "bottom", "left"] = "auto",
    options: Optional[dict[str, Any]] = None,
    **kwargs: TagAttrValue,
) -> Tag:
    """Deprecated. Please use `shiny.ui.popover()` instead."""
    warn_deprecated(
        "`shiny.experimental.ui.popover()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.ui.popover` instead."
    )
    return main_popover(
        trigger,
        *args,
        title=title,
        id=id,
        placement=placement,
        options=options,
        **kwargs,
    )


# Deprecated 2023-09-12
def toggle_popover(
    id: str,
    show: Optional[bool] = None,
    session: Optional[Session] = None,
) -> None:
    """Deprecated. Please use `shiny.ui.toggle_popover()` instead."""
    warn_deprecated(
        "`shiny.experimental.ui.toggle_popover()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.ui.toggle_popover` instead."
    )
    return main_toggle_popover(id, show, session=session)


# Deprecated 2023-09-12
def update_popover(
    id: str,
    *args: TagChild,
    title: Optional[TagChild] = None,
    session: Optional[Session] = None,
) -> None:
    """Deprecated. Please use `shiny.ui.update_popover()` instead."""
    warn_deprecated(
        "`shiny.experimental.ui.update_popover()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.ui.update_popover` instead."
    )
    return main_update_popover(id, *args, title=title, session=session)


# ######################
# # Accordion
# ######################


# # Deprecated 2023-09-12
# class AccordionPanel(MainAccordionPanel):
#     """
#     Deprecated. Please use `shiny.ui.AccordionPanel` instead.
#     """

#     ...


# # Deprecated 2023-09-12
# def accordion(
#     *args: AccordionPanel | TagAttrs,
#     id: Optional[str] = None,
#     open: Optional[bool | str | list[str]] = None,
#     multiple: bool = True,
#     class_: Optional[str] = None,
#     width: Optional[CssUnit] = None,
#     height: Optional[CssUnit] = None,
#     **kwargs: TagAttrValue,
# ) -> Tag:
#     """Deprecated. Please use `shiny.ui.accordion()` instead."""
#     warn_deprecated(
#         "`shiny.experimental.ui.accordion()` is deprecated. "
#         "This method will be removed in a future version, "
#         "please use :func:`shiny.ui.accordion` instead."
#     )
#     return main_accordion(
#         *args,
#         id=id,
#         open=open,
#         multiple=multiple,
#         class_=class_,
#         width=width,
#         height=height,
#         **kwargs,
#     )


# # Deprecated 2023-09-12
# def accordion_panel(
#     title: TagChild,
#     *args: TagChild | TagAttrs,
#     value: Optional[str] | MISSING_TYPE = MISSING,
#     icon: Optional[TagChild] = None,
#     **kwargs: TagAttrValue,
# ) -> AccordionPanel:
#     """Deprecated. Please use `shiny.ui.accordion_panel()` instead."""
#     warn_deprecated(
#         "`shiny.experimental.ui.accordion_panel()` is deprecated. "
#         "This method will be removed in a future version, "
#         "please use :func:`shiny.ui.accordion_panel` instead."
#     )
#     return main_accordion_panel(
#         title,
#         *args,
#         value=value,
#         icon=icon,
#         **kwargs,
#     )


# # Deprecated 2023-09-12
# def accordion_panel_set(
#     id: str,
#     values: bool | str | list[str],
#     session: Optional[Session] = None,
# ) -> None:
#     """Deprecated. Please use `shiny.ui.accordion_panel_set()` instead."""
#     warn_deprecated(
#         "`shiny.experimental.ui.accordion_panel_set()` is deprecated. "
#         "This method will be removed in a future version, "
#         "please use :func:`shiny.ui.accordion_panel_set` instead."
#     )
#     return main_accordion_panel_set(id, values, session=session)


# # Deprecated 2023-09-12
# def accordion_panel_open(
#     id: str,
#     values: bool | str | list[str],
#     session: Optional[Session] = None,
# ) -> None:
#     """Deprecated. Please use `shiny.ui.accordion_panel_open()` instead."""
#     warn_deprecated(
#         "`shiny.experimental.ui.accordion_panel_open()` is deprecated. "
#         "This method will be removed in a future version, "
#         "please use :func:`shiny.ui.accordion_panel_open` instead."
#     )
#     return main_accordion_panel_open(id, values, session=session)


# # Deprecated 2023-09-12
# def accordion_panel_close(
#     id: str,
#     values: bool | str | list[str],
#     session: Optional[Session] = None,
# ) -> None:
#     """Deprecated. Please use `shiny.ui.accordion_panel_close()` instead."""
#     warn_deprecated(
#         "`shiny.experimental.ui.accordion_panel_close()` is deprecated. "
#         "This method will be removed in a future version, "
#         "please use :func:`shiny.ui.accordion_panel_close` instead."
#     )
#     return main_accordion_panel_close(id, values, session=session)


# # Deprecated 2023-09-12
# def accordion_panel_insert(
#     id: str,
#     panel: AccordionPanel,
#     target: Optional[str] = None,
#     position: Literal["after", "before"] = "after",
#     session: Optional[Session] = None,
# ) -> None:
#     """Deprecated. Please use `shiny.ui.accordion_panel_insert()` instead."""
#     warn_deprecated(
#         "`shiny.experimental.ui.accordion_panel_insert()` is deprecated. "
#         "This method will be removed in a future version, "
#         "please use :func:`shiny.ui.accordion_panel_insert` instead."
#     )
#     return main_accordion_panel_insert(
#         id,
#         panel,
#         target=target,
#         position=position,
#         session=session,
#     )


# # Deprecated 2023-09-12
# def accordion_panel_remove(
#     id: str,
#     target: str | list[str],
#     session: Optional[Session] = None,
# ) -> None:
#     """Deprecated. Please use `shiny.ui.accordion_panel_remove()` instead."""
#     warn_deprecated(
#         "`shiny.experimental.ui.accordion_panel_remove()` is deprecated. "
#         "This method will be removed in a future version, "
#         "please use :func:`shiny.ui.accordion_panel_remove` instead."
#     )
#     return main_accordion_panel_remove(
#         id,
#         target=target,
#         session=session,
#     )


# # Deprecated 2023-09-12
# def update_accordion_panel(
#     id: str,
#     target: str,
#     *body: TagChild,
#     title: TagChild | None | MISSING_TYPE = MISSING,
#     value: str | None | MISSING_TYPE = MISSING,
#     icon: TagChild | None | MISSING_TYPE = MISSING,
#     session: Optional[Session] = None,
# ) -> None:
#     """Deprecated. Please use `shiny.ui.update_accordion_panel()` instead."""
#     warn_deprecated(
#         "`shiny.experimental.ui.update_accordion_panel()` is deprecated. "
#         "This method will be removed in a future version, "
#         "please use :func:`shiny.ui.update_accordion_panel` instead."
#     )
#     return main_update_accordion_panel(
#         id,
#         target,
#         *body,
#         title=title,
#         value=value,
#         icon=icon,
#         session=session,
#     )


# ######################
# # Fill
# ######################
TagT = TypeVar("TagT", bound="Tag")


def as_fill_carrier(
    tag: TagT,
    *,
    min_height: None = None,
    max_height: None = None,
    gap: None = None,
) -> TagT:
    """Deprecated. Please use `shiny.ui.fill.as_fill_carrier()` instead."""
    warn_deprecated(
        "`shiny.experimental.ui.as_fill_carrier()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.ui.fill.as_fill_carrier` instead."
    )

    if min_height is not None:
        raise RuntimeError(
            "`min_height` is no longer supported. Please add the attribute directly to the Tag's style."
        )
    if max_height is not None:
        raise RuntimeError(
            "`max_height` is no longer supported. Please add the attribute directly to the Tag's style."
        )
    if gap is not None:
        raise RuntimeError(
            "`gap` is no longer supported. Please add the attribute directly to the Tag's style."
        )

    return main_as_fill_carrier(tag)


def as_fillable_container(
    tag: TagT,
    *,
    min_height: None = None,
    max_height: None = None,
    gap: None = None,
) -> TagT:
    """Deprecated. Please use `shiny.ui.fill.as_fillable_container()` instead."""
    warn_deprecated(
        "`shiny.experimental.ui.as_fillable_container()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.ui.fill.as_fillable_container` instead."
    )
    if min_height is not None:
        raise RuntimeError(
            "`min_height` is no longer supported. Please add the attribute directly to the Tag's style."
        )
    if max_height is not None:
        raise RuntimeError(
            "`max_height` is no longer supported. Please add the attribute directly to the Tag's style."
        )
    if gap is not None:
        raise RuntimeError(
            "`gap` is no longer supported. Please add the attribute directly to the Tag's style."
        )

    return main_as_fillable_container(tag)


def as_fill_item(
    tag: TagT,
    *,
    min_height: None = None,
    max_height: None = None,
) -> TagT:
    """Deprecated. Please use `shiny.ui.fill.as_fill_item()` instead."""
    warn_deprecated(
        "`shiny.experimental.ui.as_fill_item()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.ui.fill.as_fill_item` instead."
    )
    if min_height is not None:
        raise RuntimeError(
            "`min_height` is no longer supported. Please add the attribute directly to the Tag's style."
        )
    if max_height is not None:
        raise RuntimeError(
            "`max_height` is no longer supported. Please add the attribute directly to the Tag's style."
        )

    return main_as_fill_item(tag)


def remove_all_fill(tag: TagT) -> TagT:
    """Deprecated. Please use `shiny.ui.fill.remove_all_fill()` instead."""
    warn_deprecated(
        "`shiny.experimental.ui.remove_all_fill()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.ui.fill.remove_all_fill` instead."
    )
    return main_remove_all_fill(tag)


def is_fill_carrier(tag: Tag) -> bool:
    """Deprecated. Please use `shiny.ui.fill.is_fill_carrier()` instead."""
    warn_deprecated(
        "`shiny.experimental.ui.is_fill_carrier()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.ui.fill.is_fill_carrier` instead."
    )
    return main_is_fill_carrier(tag)


def is_fillable_container(tag: TagChild) -> bool:
    """Deprecated. Please use `shiny.ui.fill.is_fillable_container()` instead."""
    warn_deprecated(
        "`shiny.experimental.ui.is_fillable_container()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.ui.fill.is_fillable_container` instead."
    )
    return main_is_fillable_container(tag)


def is_fill_item(tag: TagChild) -> bool:
    """Deprecated. Please use `shiny.ui.fill.is_fill_item()` instead."""
    warn_deprecated(
        "`shiny.experimental.ui.is_fill_item()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.ui.fill.is_fill_item` instead."
    )
    return main_is_fill_item(tag)


# ######################
# # Card
# ######################

TagCallable = TagFunction
"""Deprecated. Please use `htmltools.TagFunction"""

WrapperCallable = MainWrapperCallable
"""Deprecated. Please use `shiny.ui.WrapperCallable` instead."""


class CardItem(MainCardItem):
    """Deprecated. Please use `shiny.ui.CardItem` instead."""

    def __init__(
        self,
        item: TagChild,
    ):
        warn_deprecated(
            "`shiny.experimental.ui.CardItem()` is deprecated. "
            "This class will be removed in a future version, "
            "please use :class:`shiny.ui.CardItem` instead."
        )
        super().__init__(item)


# TODO-maindocs; @add_example()
def card_header(
    *args: TagChild | TagAttrs,
    container: TagFunction = tags.div,
    **kwargs: TagAttrValue,
) -> MainCardItem:
    """Deprecated. Please use `shiny.ui.card_header()` instead."""
    warn_deprecated(
        "`shiny.experimental.ui.card_header()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.ui.card_header` instead."
    )
    return main_card_header(*args, container=container, **kwargs)


def card_footer(
    *args: TagChild | TagAttrs,
    **kwargs: TagAttrValue,
) -> MainCardItem:
    """Deprecated. Please use `shiny.ui.card_footer()` instead."""
    warn_deprecated(
        "`shiny.experimental.ui.card_footer()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.ui.card_footer` instead."
    )

    return main_card_footer(*args, **kwargs)


# ######################
# # Layout
# ######################
def layout_column_wrap(
    width: Optional[CssUnit],
    *args: TagChild | TagAttrs,
    fixed_width: bool = False,
    heights_equal: Literal["all", "row"] = "all",
    fill: bool = True,
    fillable: bool = True,
    height: Optional[CssUnit] = None,
    height_mobile: Optional[CssUnit] = None,
    gap: Optional[CssUnit] = None,
    class_: Optional[str] = None,
    **kwargs: TagAttrValue,
) -> Tag:
    """Deprecated. Please use `shiny.ui.layout_column_wrap()` instead."""
    warn_deprecated(
        "`shiny.experimental.ui.layout_column_wrap()` is deprecated. "
        "This method will be removed in a future version, "
        "please use :func:`shiny.ui.layout_column_wrap` instead."
    )
    return main_layout_column_wrap(
        width,
        *args,
        fixed_width=fixed_width,
        heights_equal=heights_equal,
        fill=fill,
        fillable=fillable,
        height=height,
        height_mobile=height_mobile,
        gap=gap,
        class_=class_,
        **kwargs,
    )
