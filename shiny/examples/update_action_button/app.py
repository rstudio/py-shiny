from shiny import *
from htmltools import br
from fontawesome import icon_svg as icon

app_ui = ui.page_fluid(
    ui.input_action_button("update", "Update other buttons and link"),
    br(),
    ui.input_action_button("goButton", "Go"),
    br(),
    ui.input_action_button("goButton2", "Go 2", icon=icon("bars")),
    br(),
    ui.input_action_button("goButton3", "Go 3"),
    br(),
    ui.input_action_link("goLink", "Go Link"),
)


def server(input: Inputs, output: Outputs, session: Session):
    @reactive.Effect
    def _():
        req(input.update())
        # Updates goButton's label and icon
        ui.update_action_button("goButton", label="New label", icon=icon("calendar"))
        # Leaves goButton2's label unchanged and removes its icon
        ui.update_action_button("goButton2", icon=[])
        # Leaves goButton3's icon, if it exists, unchanged and changes its label
        ui.update_action_button("goButton3", label="New label 3")
        # Updates goLink's label and icon
        ui.update_action_link("goLink", label="New link label", icon=icon("link"))


app = App(app_ui, server)
