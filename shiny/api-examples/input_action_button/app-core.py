import matplotlib.pyplot as plt
import numpy as np

from shiny import App, Inputs, Outputs, Session, reactive, render, ui

app_ui = ui.page_fluid(
    ui.input_slider("n", "Number of observations", min=0, max=1000, value=500),
    ui.input_action_button("go", "Go!", class_="btn-success"),
    ui.output_plot("plot"),
)


def server(input: Inputs, output: Outputs, session: Session):
    @render.plot(alt="A histogram")
    # Use reactive.event() to invalidate the plot only when the button is pressed
    # (not when the slider is changed)
    @reactive.event(input.go, ignore_none=False)
    def plot():
        x = 100 + 15 * np.random.default_rng(seed=19680801).randn(input.n())
        fig, ax = plt.subplots()
        ax.hist(x, bins=30, density=True)
        return fig


app = App(app_ui, server)
