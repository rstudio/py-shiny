from __future__ import annotations

import shiny.experimental as x
from shiny import App, ui

app_ui = ui.page_fluid(x.ui.layout_sidebar("Main content", sidebar="Sidebar content"))


app = App(app_ui, server=None)
