# This app demonstrates how to use "global" variables that are shared across sessions.
# This is useful if you want to load data just once and use it in multiple apps, or if
# you want to share data or reactives among apps.

import matplotlib.pyplot as plt
import numpy as np
import shared

from shiny import reactive, render, ui
from shiny.express import input

ui.input_slider("n", "N", 1, 100, 50)


@render.plot
def histogram():
    np.random.seed(19680801)
    x = 100 + 15 * np.random.randn(437)
    plt.hist(x, shared.rv(), density=True)


@reactive.Effect
def _():
    shared.rv.set(input.n())


@render.text
def rv_value():
    return f"Shared rv = {shared.rv.get()}"
