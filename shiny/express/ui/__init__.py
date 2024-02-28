from __future__ import annotations


from htmltools import (
    TagList,
    Tag,
    TagChild,
    TagAttrs,
    TagAttrValue,
    tags,
    HTML,
    head_content,
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
    hr,
    img,
    p,
    pre,
    span,
    strong,
)

from ...ui import (
    fill,
)

from ...ui import (
    AccordionPanel,
    AnimationOptions,
    CardItem,
    ShowcaseLayout,
    Sidebar,
    SliderStepArg,
    SliderValueArg,
    ValueBoxTheme,
    brush_opts,
    click_opts,
    dblclick_opts,
    help_text,
    hover_opts,
    include_css,
    include_js,
    input_action_button,
    input_action_link,
    input_checkbox,
    input_checkbox_group,
    input_switch,
    input_radio_buttons,
    input_dark_mode,
    input_date,
    input_date_range,
    input_file,
    input_numeric,
    input_password,
    input_select,
    input_selectize,
    input_slider,
    bind_task_button,
    input_task_button,
    input_text,
    input_text_area,
    panel_title,
    insert_accordion_panel,
    remove_accordion_panel,
    update_accordion,
    update_accordion_panel,
    update_sidebar,
    update_action_button,
    update_action_link,
    update_checkbox,
    update_switch,
    update_checkbox_group,
    update_radio_buttons,
    update_dark_mode,
    update_date,
    update_date_range,
    update_numeric,
    update_select,
    update_selectize,
    update_slider,
    update_task_button,
    update_text,
    update_text_area,
    update_navs,
    update_tooltip,
    update_popover,
    insert_ui,
    remove_ui,
    markdown,
    modal_button,
    modal,
    modal_show,
    modal_remove,
    notification_show,
    notification_remove,
    nav_spacer,
    Progress,
    value_box_theme,
    js_eval,
)

from ._cm_components import (
    sidebar,
    layout_sidebar,
    layout_column_wrap,
    layout_columns,
    card,
    card_header,
    card_footer,
    accordion,
    accordion_panel,
    nav_panel,
    nav_control,
    nav_menu,
    navset_bar,
    navset_card_pill,
    navset_card_tab,
    navset_card_underline,
    navset_hidden,
    navset_pill,
    navset_pill_list,
    navset_tab,
    navset_underline,
    value_box,
    panel_well,
    panel_conditional,
    panel_fixed,
    panel_absolute,
    tooltip,
    popover,
)

from ._page import (
    page_opts,
)

from ._hold import (
    hold,
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
    "fill",
    # Imports from ...ui
    "AccordionPanel",
    "AnimationOptions",
    "CardItem",
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
    "value_box_theme",
    # Imports from ._cm_components
    "sidebar",
    "layout_sidebar",
    "layout_column_wrap",
    "layout_columns",
    "card",
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
        "nav",  # Deprecated in favor of nav_panel
        "navset_pill_card",  # Deprecated
        "navset_tab_card",  # Deprecated
        "page_bootstrap",
        "page_fixed",
        "page_sidebar",
        "page_fillable",
        "page_navbar",
        "page_fluid",
        "page_auto",
        "page_output",
        "panel_main",  # Deprecated
        "panel_sidebar",  # Deprecated
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
    ),
    # Items from shiny.express.ui that don't have a counterpart in shiny.ui
    "shiny.express.ui": (
        "page_opts",
        "hold",
    ),
}
