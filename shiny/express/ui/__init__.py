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
    AccordionPanel,
    AnimationOptions,
    CardItem,
    card_header,
    card_footer,
    ShowcaseLayout,
    Sidebar,
    SliderStepArg,
    SliderValueArg,
    ValueBoxTheme,
    download_button,
    download_link,
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
    input_date,
    input_date_range,
    input_file,
    input_numeric,
    input_password,
    input_select,
    input_selectize,
    input_slider,
    input_text,
    input_text_area,
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
    update_date,
    update_date_range,
    update_numeric,
    update_select,
    update_selectize,
    update_slider,
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
    output_plot,
    output_image,
    output_text,
    output_text_verbatim,
    output_table,
    output_ui,
    Progress,
    output_data_frame,
    value_box_theme,
)

from ._cm_components import (
    set_page,
    sidebar,
    layout_sidebar,
    layout_column_wrap,
    column,
    row,
    card,
    accordion,
    accordion_panel,
    navset,
    navset_card,
    nav,
    nav_control,
    nav_menu,
    value_box,
    panel_well,
    panel_conditional,
    panel_fixed,
    panel_absolute,
    page_fluid,
    page_fixed,
    page_fillable,
    page_sidebar,
    page_navbar,
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
    # Imports from ...ui
    "AccordionPanel",
    "AnimationOptions",
    "CardItem",
    "ShowcaseLayout",
    "Sidebar",
    "SliderStepArg",
    "SliderValueArg",
    "ValueBoxTheme",
    "card_header",
    "card_footer",
    "download_button",
    "download_link",
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
    "input_date",
    "input_date_range",
    "input_file",
    "input_numeric",
    "input_password",
    "input_select",
    "input_selectize",
    "input_slider",
    "input_text",
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
    "update_date",
    "update_date_range",
    "update_numeric",
    "update_select",
    "update_selectize",
    "update_slider",
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
    "output_plot",
    "output_image",
    "output_text",
    "output_text_verbatim",
    "output_table",
    "output_ui",
    "Progress",
    "output_data_frame",
    "value_box_theme",
    # Imports from ._cm_components
    "set_page",
    "sidebar",
    "layout_sidebar",
    "layout_column_wrap",
    "column",
    "row",
    "card",
    "accordion",
    "accordion_panel",
    "navset",
    "navset_card",
    "nav",
    "nav_control",
    "nav_menu",
    "value_box",
    "panel_well",
    "panel_conditional",
    "panel_fixed",
    "panel_absolute",
    "page_fluid",
    "page_fixed",
    "page_fillable",
    "page_sidebar",
    "page_navbar",
)


_known_missing = {
    # Items from shiny.ui that don't have a counterpart in shiny.express.ui
    "shiny.ui": (
        "navset_bar",
        "navset_card_pill",
        "navset_card_tab",
        "navset_card_underline",
        "navset_hidden",
        "navset_pill",
        "navset_pill_card",
        "navset_pill_list",
        "navset_tab",
        "navset_tab_card",
        "navset_underline",
        "page_bootstrap",
        "page_output",
        "panel_main",  # Deprecated
        "panel_sidebar",  # Deprecated
        "panel_title",
        "popover",
        "showcase_bottom",
        "showcase_left_center",
        "showcase_top_right",
        "tooltip",
    ),
    # Items from shiny.express.ui that don't have a counterpart in shiny.ui
    "shiny.express.ui": (
        "set_page",
        # TODO: Migrate these to shiny.ui
        "navset",
        "navset_card",
    ),
}
