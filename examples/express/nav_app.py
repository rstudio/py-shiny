import matplotlib.pyplot as plt
import numpy as np

from shiny import render
from shiny.express import input, ui

with ui.layout_column_wrap(width=1 / 2):
    with ui.navset_underline():
        with ui.nav_panel(title="One"):
            ui.input_slider("n", "N", 1, 100, 50)

        with ui.nav_panel(title="Two"):

            @render.plot
            def histogram():
                x = 100 + 15 * np.random.RandomState(seed=19680801).randn(437)
                plt.hist(x, input.n(), density=True)

    with ui.navset_card_underline():
        with ui.nav_panel(title="One"):
            ui.input_slider("n2", "N", 1, 100, 50)

        with ui.nav_panel(title="Two"):

            @render.plot
            def histogram2():
                x = 100 + 15 * np.random.RandomState(seed=19680801).randn(437)
                plt.hist(x, input.n2(), density=True)
