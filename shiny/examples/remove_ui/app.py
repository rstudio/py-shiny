from shiny import *

app_ui = ui.page_fluid(
    ui.input_action_button("rmv", "Remove UI"),
    ui.input_text("txt", "Click button above to remove me"),
)


def server(input: Inputs, output: Outputs, session: Session):
    @reactive.Effect
    @event(input.rmv)
    def _():
        ui.remove_ui(selector="div:has(> #txt)")


app = App(app_ui, server)
