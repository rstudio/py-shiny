from shiny.express import ui

with ui.navset_card_tab(id="tab"):
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
