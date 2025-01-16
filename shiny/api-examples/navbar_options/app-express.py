from shiny.express import input, render, ui

with ui.navset_bar(
    title="Navset Bar",
    id="selected_navset_bar",
    navbar_options=ui.navbar_options(
        bg="#B73A85",
        theme="dark",
        underline=False,
    ),
):
    with ui.nav_panel("A"):
        "Panel A content"

    with ui.nav_panel("B"):
        "Panel B content"

    with ui.nav_panel("C"):
        "Panel C content"

    with ui.nav_menu("Other links"):
        with ui.nav_panel("D"):
            "Page D content"

        "----"
        "Description:"
        with ui.nav_control():
            ui.a("Shiny", href="https://shiny.posit.co", target="_blank")
ui.h5("Selected:")


@render.code
def _():
    return input.selected_navset_bar()
