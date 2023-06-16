"""
Tools for creating user interfaces including: custom components, HTML components,
layout helpers, page-level containers, and more.
"""

from ._bootstrap import (
    row,
    column,
    layout_sidebar,
    panel_well,
    panel_sidebar,
    panel_main,
    panel_conditional,
    panel_title,
    panel_fixed,
    panel_absolute,
    help_text,
)
from ._download_button import download_button, download_link
from ._plot_output_opts import brush_opts, click_opts, dblclick_opts, hover_opts
from ._include_helpers import include_css, include_js
from ._input_action_button import input_action_button, input_action_link
from ._input_check_radio import (
    input_checkbox,
    input_checkbox_group,
    input_switch,
    input_radio_buttons,
)
from ._input_date import input_date, input_date_range
from ._input_file import input_file
from ._input_numeric import input_numeric
from ._input_password import input_password
from ._input_select import input_select, input_selectize
from ._input_slider import input_slider, SliderValueArg, SliderStepArg, AnimationOptions
from ._input_text import input_text, input_text_area
from ._input_update import (
    update_action_button,
    update_action_link,
    update_checkbox,
    update_switch,
    update_checkbox_group,
    update_radio_buttons,
    update_date,
    update_date_range,
    update_numeric,
    update_select,
    update_selectize,
    update_slider,
    update_text,
    update_text_area,
    update_navs,
)
from ._insert import insert_ui, remove_ui
from ._markdown import markdown
from ._modal import modal_button, modal, modal_show, modal_remove
from ._navs import (
    nav,
    nav_menu,
    nav_control,
    nav_spacer,
    navset_tab,
    navset_tab_card,
    navset_pill,
    navset_pill_card,
    navset_pill_list,
    navset_hidden,
    navset_bar,
)
from ._notification import notification_show, notification_remove
from ._output import (
    output_plot,
    output_image,
    output_text,
    output_text_verbatim,
    output_table,
    output_ui,
)
from ._page import page_navbar, page_fluid, page_fixed, page_bootstrap
from ._progress import Progress

from .dataframe._dataframe import output_data_frame

from htmltools import (
    TagList,
    Tag,
    TagChild,
    TagAttrs,
    TagAttrValue,
    tags,
    HTML,
    head_content,
    p,
    h1,
    h2,
    h3,
    h4,
    h5,
    h6,
    a,
    br,
    div,
    span,
    pre,
    code,
    img,
    strong,
    em,
    hr,
)


__all__ = (
    "row",
    "column",
    "layout_sidebar",
    "panel_well",
    "panel_sidebar",
    "panel_main",
    "panel_conditional",
    "panel_title",
    "panel_fixed",
    "panel_absolute",
    "help_text",
    "download_button",
    "download_link",
    "brush_opts",
    "click_opts",
    "dblclick_opts",
    "hover_opts",
    "include_css",
    "include_js",
    "input_action_button",
    "input_action_link",
    "input_checkbox",
    "input_checkbox_group",
    "input_switch",
    "input_radio_buttons",
    "input_date",
    "input_date_range",
    "input_file",
    "input_numeric",
    "input_password",
    "input_select",
    "input_selectize",
    "input_slider",
    "SliderValueArg",
    "SliderStepArg",
    "AnimationOptions",
    "input_text",
    "input_text_area",
    "update_action_button",
    "update_action_link",
    "update_checkbox",
    "update_switch",
    "update_checkbox_group",
    "update_radio_buttons",
    "update_date",
    "update_date_range",
    "update_numeric",
    "update_select",
    "update_selectize",
    "update_slider",
    "update_text",
    "update_text_area",
    "update_navs",
    "insert_ui",
    "remove_ui",
    "markdown",
    "modal_button",
    "modal",
    "modal_show",
    "modal_remove",
    "nav",
    "nav_menu",
    "nav_control",
    "nav_spacer",
    "navset_tab",
    "navset_tab_card",
    "navset_pill",
    "navset_pill_card",
    "navset_pill_list",
    "navset_hidden",
    "navset_bar",
    "notification_show",
    "notification_remove",
    "output_data_frame",
    "output_plot",
    "output_image",
    "output_text",
    "output_text_verbatim",
    "output_table",
    "output_ui",
    "page_navbar",
    "page_fluid",
    "page_fixed",
    "page_bootstrap",
    "Progress",
    # Items below are from htmltools
    "TagList",
    "Tag",
    "TagChild",
    "TagAttrs",
    "TagAttrValue",
    "tags",
    "HTML",
    "head_content",
    "p",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "a",
    "br",
    "div",
    "span",
    "pre",
    "code",
    "img",
    "strong",
    "em",
    "hr",
)
