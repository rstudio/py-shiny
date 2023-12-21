from shiny import render, ui
from shiny.express import input, ui

ui.set_page(ui.page_fillable())

with ui.card(id="card"):
    ui.input_slider("a", "A", 1, 100, 50)

    @render.text
    def txt():
        return input.a()
