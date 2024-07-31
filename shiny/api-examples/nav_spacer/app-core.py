from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.navset_underline(
        ui.nav_panel("A", "Panel A content"),
        ui.nav_spacer(),
        ui.nav_panel("B", "Panel B content"),
        ui.nav_panel("C", "Panel C content"),
        id="selected_navset_underline",
    ),
    ui.h5("Selected:"),
    ui.output_code("debug"),
)


def server(input, output, session):
    @render.code
    def debug():
        return input.selected_navset_underline()


app = App(app_ui, server)
