import matplotlib.pyplot as plt
import numpy as np

from shiny import render
from shiny.express import input, ui

with ui.layout_column_wrap(width=1 / 2):
    with ui.card():
        ui.input_slider("n", "N", 1, 100, 50)

    with ui.card():

        @render.plot
        def histogram():
            x = 100 + 15 * np.random.RandomState(seed=19680801).randn(437)
            plt.hist(x, input.n(), density=True)

    with ui.card():

        @render.plot
        def histogram2():
            x = 100 + 15 * np.random.RandomState(seed=19680801).randn(437)
            plt.hist(x, input.n(), density=True, color="red")
