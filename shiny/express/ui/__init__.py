from __future__ import annotations

from htmltools import (
    HTML,
    Tag,
    TagAttrs,
    TagAttrValue,
    TagChild,
    TagList,
    a,
    br,
    code,
    div,
    em,
    h1,
    h2,
    h3,
    h4,
    h5,
    h6,
    head_content,
    hr,
    img,
    p,
    pre,
    span,
    strong,
    tags,
)

from ...ui import (
    AccordionPanel,
    AnimationOptions,
    CardItem,
    Chat,
    Progress,
    ShowcaseLayout,
    Sidebar,
    SliderStepArg,
    SliderValueArg,
    Theme,
    ValueBoxTheme,
    bind_task_button,
    brush_opts,
    busy_indicators,
    click_opts,
    dblclick_opts,
    fill,
    help_text,
    hover_opts,
    include_css,
    include_js,
    input_action_button,
    input_action_link,
    input_checkbox,
    input_checkbox_group,
    input_dark_mode,
    input_date,
    input_date_range,
    input_file,
    input_numeric,
    input_password,
    input_radio_buttons,
    input_select,
    input_selectize,
    input_slider,
    input_switch,
    input_task_button,
    input_text,
    input_text_area,
    insert_accordion_panel,
    insert_ui,
    js_eval,
    markdown,
    modal,
    modal_button,
    modal_remove,
    modal_show,
    nav_spacer,
    notification_remove,
    notification_show,
    panel_title,
    remove_accordion_panel,
    remove_ui,
    update_accordion,
    update_accordion_panel,
    update_action_button,
    update_action_link,
    update_checkbox,
    update_checkbox_group,
    update_dark_mode,
    update_date,
    update_date_range,
    update_navs,
    update_numeric,
    update_popover,
    update_radio_buttons,
    update_select,
    update_selectize,
    update_sidebar,
    update_slider,
    update_switch,
    update_task_button,
    update_text,
    update_text_area,
    update_tooltip,
    value_box_theme,
)
from ._cm_components import (
    accordion,
    accordion_panel,
    card,
    card_body,
    card_footer,
    card_header,
    layout_column_wrap,
    layout_columns,
    layout_sidebar,
    nav_control,
    nav_menu,
    nav_panel,
    navset_bar,
    navset_card_pill,
    navset_card_tab,
    navset_card_underline,
    navset_hidden,
    navset_pill,
    navset_pill_list,
    navset_tab,
    navset_underline,
    panel_absolute,
    panel_conditional,
    panel_fixed,
    panel_well,
    popover,
    sidebar,
    tooltip,
    value_box,
)
from ._hold import (
    hold,
)
from ._page import (
    page_opts,
)

__all__ = (
    # Imports from htmltools
    "TagList",
    "Tag",
    "TagChild",
    "TagAttrs",
    "TagAttrValue",
    "tags",
    "HTML",
    "head_content",
    "a",
    "br",
    "code",
    "div",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "img",
    "p",
    "pre",
    "span",
    "strong",
    "tags",
    # Submodules
    "busy_indicators",
    "fill",
    # Imports from ...ui
    "AccordionPanel",
    "AnimationOptions",
    "CardItem",
    "Chat",
    "ShowcaseLayout",
    "Sidebar",
    "SliderStepArg",
    "SliderValueArg",
    "ValueBoxTheme",
    "brush_opts",
    "click_opts",
    "dblclick_opts",
    "help_text",
    "hover_opts",
    "include_css",
    "include_js",
    "input_action_button",
    "input_action_link",
    "input_checkbox",
    "input_checkbox_group",
    "input_switch",
    "input_radio_buttons",
    "input_dark_mode",
    "input_date",
    "input_date_range",
    "input_file",
    "input_numeric",
    "input_password",
    "input_select",
    "input_selectize",
    "input_slider",
    "bind_task_button",
    "input_task_button",
    "input_text",
    "panel_title",
    "input_text_area",
    "insert_accordion_panel",
    "remove_accordion_panel",
    "update_accordion",
    "update_accordion_panel",
    "update_sidebar",
    "update_action_button",
    "update_action_link",
    "update_checkbox",
    "update_switch",
    "update_checkbox_group",
    "update_radio_buttons",
    "update_dark_mode",
    "update_date",
    "update_date_range",
    "update_numeric",
    "update_select",
    "update_selectize",
    "update_slider",
    "update_task_button",
    "update_text",
    "update_text_area",
    "update_navs",
    "update_tooltip",
    "update_popover",
    "insert_ui",
    "remove_ui",
    "markdown",
    "modal_button",
    "modal",
    "modal_show",
    "modal_remove",
    "notification_show",
    "notification_remove",
    "nav_spacer",
    "Progress",
    "Theme",
    "value_box_theme",
    # Imports from ._cm_components
    "sidebar",
    "layout_sidebar",
    "layout_column_wrap",
    "layout_columns",
    "card",
    "card_body",
    "card_header",
    "card_footer",
    "accordion",
    "accordion_panel",
    "nav_panel",
    "nav_control",
    "nav_menu",
    "navset_bar",
    "navset_card_pill",
    "navset_card_tab",
    "navset_card_underline",
    "navset_hidden",
    "navset_pill",
    "navset_pill_list",
    "navset_tab",
    "navset_underline",
    "value_box",
    "panel_well",
    "panel_conditional",
    "panel_fixed",
    "panel_absolute",
    "popover",
    "tooltip",
    # Imports from ._page
    "page_opts",
    # Imports from ._hold
    "hold",
    "js_eval",
)


# This is used for unit tests to verify that shiny.ui and shiny.express.ui stay in sync.
_known_missing = {
    # Items from shiny.ui that don't have a counterpart in shiny.express.ui
    "shiny.ui": (
        "column",  # Deprecated in favor of layout_columns
        "row",  # Deprecated in favor of layout_columns
        "page_bootstrap",
        "page_fixed",
        "page_sidebar",
        "page_fillable",
        "page_navbar",
        "page_fluid",
        "page_auto",
        "page_output",
        "showcase_bottom",
        "showcase_left_center",
        "showcase_top_right",
        # Outputs automatically placed by render functions
        "download_button",
        "download_link",
        "output_plot",
        "output_image",
        "output_text",
        "output_code",
        "output_text_verbatim",
        "output_table",
        "output_ui",
        "output_data_frame",
        # Chat knows how to render itself in express
        "chat_ui",
    ),
    # Items from shiny.express.ui that don't have a counterpart in shiny.ui
    "shiny.express.ui": (
        "page_opts",
        "hold",
    ),
}
