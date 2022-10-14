from shiny import App, reactive, render, ui

app_ui = ui.page_fluid(
    ui.input_numeric("x", "Enter a value to add to the list:", 1),
    ui.input_action_button("submit", "Add Value"),
    ui.p(
        ui.output_text_verbatim("out")
    ),
)

def server(input, output, session):
    # Stores all the values the user has submitted so far
    user_provided_values = reactive.Value([])

    @reactive.Effect
    @reactive.event(input.submit)
    def add_value_to_list():
        user_provided_values.set(user_provided_values() + [input.x()])

    @reactive.Calc
    def doubled_values():
        return [x*2 for x in user_provided_values()]

    @output
    @render.text
    def out():
        return f"Raw Values: {user_provided_values()}\n" + f"Doubled: {doubled_values()}"

app = App(app_ui, server)
