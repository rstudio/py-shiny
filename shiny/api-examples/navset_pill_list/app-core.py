from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.navset_pill_list(
        ui.nav_panel("A", "Panel A content"),
        ui.nav_panel("B", "Panel B content"),
        ui.nav_panel("C", "Panel C content"),
        ui.nav_menu(
            "Other links",
            ui.nav_panel("D", "Panel D content"),
            "----",
            "Description:",
            ui.nav_control(
                ui.a("Shiny", href="https://shiny.posit.co", target="_blank")
            ),
        ),
        id="selected_navset_pill_list",
    ),
    ui.h5("Selected:"),
    ui.output_code("debug"),
)


def server(input, output, session):
    @render.code
    def debug():
        return input.selected_navset_pill_list()


app = App(app_ui, server)
