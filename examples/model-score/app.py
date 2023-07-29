import sqlite3
from datetime import datetime, timedelta, timezone

import pandas as pd
import plotly.express as px
import scoredata
from plotly_streaming import render_plotly_streaming
from shinywidgets import output_widget

import shiny.experimental as x
from shiny import App, Inputs, Outputs, Session, reactive, render, ui

# TODO: Make an option to switch between dynamic and static
# TODO: Talk to Julia and Isabel for suggestions

THRESHOLD_MID = 0.85
THRESHOLD_MID_COLOR = "rgb(0, 137, 26)"
THRESHOLD_LOW = 0.5
THRESHOLD_LOW_COLOR = "rgb(193, 0, 0)"

# Start a background thread that writes fake data to the SQLite database every second
scoredata.begin()

con = sqlite3.connect(scoredata.SQLITE_DB_URI, uri=True)


def last_modified(con):
    return con.execute("select max(timestamp) from auc_scores").fetchone()[0]


# @reactive.poll calls a cheap query (`last_modified()`) every 1 second to check if the
# expensive query (`df()`) should be run and downstream calculations should be updated.
#
# By declaring this function at the top-level of the script instead of in the server
# function, all sessions are sharing the same reactive poll, so the expensive query is
# only run once no matter how many users are connected.


@reactive.poll(lambda: last_modified(con))
def df():
    tbl = pd.read_sql(
        "select * from auc_scores order by timestamp desc, model desc limit ?",
        con,
        params=[150],
    )
    # Treat timestamp as a continuous variable
    tbl["timestamp"] = pd.to_datetime(tbl["timestamp"], utc=True)
    tbl["time"] = tbl["timestamp"].dt.strftime("%H:%M:%S")
    # Reverse order of rows
    tbl = tbl.iloc[::-1]

    return tbl


def read_time_period(from_time, to_time):
    tbl = pd.read_sql(
        "select * from auc_scores where timestamp between ? and ? order by timestamp, model",
        con,
        params=[from_time, to_time],
    )
    # Treat timestamp as a continuous variable
    tbl["timestamp"] = pd.to_datetime(tbl["timestamp"], utc=True)
    tbl["time"] = tbl["timestamp"].dt.strftime("%H:%M:%S")

    return tbl


model_colors = {
    "model_1": "#7fc97f",
    "model_2": "#beaed4",
    "model_3": "#fdc086",
    "model_4": "#ffff99",
    "model_5": "#386cb0",
}
model_names = list(model_colors.keys())


def app_ui(req):
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=1)

    return x.ui.page_sidebar(
        x.ui.sidebar(
            ui.input_checkbox_group(
                "models", "Models", model_names, selected=model_names
            ),
            ui.input_radio_buttons(
                "timeframe",
                "Timeframe",
                ["Latest", "Specific timeframe"],
                selected="Latest",
            ),
            ui.panel_conditional(
                "input.timeframe === 'Latest'",
                ui.input_selectize(
                    "refresh",
                    "Refresh interval",
                    {
                        0: "Realtime",
                        5: "5 seconds",
                        30: "30 seconds",
                        60 * 5: "5 minutes",
                        60 * 15: "15 minutes",
                    },
                ),
            ),
            ui.panel_conditional(
                "input.timeframe !== 'Latest'",
                ui.input_slider(
                    "timerange",
                    "Time range",
                    min=start_time,
                    max=end_time,
                    value=[start_time, end_time],
                    step=timedelta(seconds=1),
                    time_format="%H:%M:%S",
                ),
            ),
        ),
        ui.div(
            ui.h1("Model monitoring dashboard"),
            ui.p(
                x.ui.output_ui("value_boxes"),
            ),
            x.ui.card(output_widget("plot_timeseries")),
            x.ui.card(output_widget("plot_dist")),
            style="max-width: 800px;",
        ),
        fillable=False,
    )


def server(input: Inputs, output: Outputs, session: Session):
    @reactive.Effect
    def update_time_range():
        reactive.invalidate_later(5)
        min_time, max_time = pd.to_datetime(
            con.execute(
                "select min(timestamp), max(timestamp) from auc_scores"
            ).fetchone(),
            utc=True,
        )
        ui.update_slider(
            "timerange",
            min=min_time.replace(tzinfo=timezone.utc),
            max=max_time.replace(tzinfo=timezone.utc),
        )

    @reactive.Calc
    def recent_df():
        refresh = int(input.refresh())
        if refresh == 0:
            return df()
        else:
            reactive.invalidate_later(refresh)
            with reactive.isolate():
                return df()

    @reactive.Calc
    def timeframe_df():
        start, end = input.timerange()
        return read_time_period(start, end)

    @reactive.Calc
    def filtered_df():
        data = recent_df() if input.timeframe() == "Latest" else timeframe_df()

        # Filter the rows so we only include the desired models
        return data[data["model"].isin(input.models())]

    @reactive.Calc
    def filtered_model_names():
        return filtered_df()["model"].unique()

    @output
    @render.ui
    def value_boxes():
        data = filtered_df()
        models = data["model"].unique().tolist()
        scores_by_model = {
            x: data[data["model"] == x].iloc[-1]["score"] for x in models
        }
        # Round scores to 2 decimal places
        scores_by_model = {x: round(y, 2) for x, y in scores_by_model.items()}

        return x.ui.layout_column_wrap(
            "135px",
            *[
                x.ui.value_box(
                    model,
                    ui.h2(score),
                    theme_color="success"
                    if score > THRESHOLD_MID
                    else "warning"
                    if score > THRESHOLD_LOW
                    else "danger",
                )
                for model, score in scores_by_model.items()
            ],
            fixed_width=True,
        )

    @output
    @render_plotly_streaming(recreate_key=filtered_model_names)
    def plot_timeseries():
        fig = px.line(
            filtered_df(),
            x="time",
            y="score",
            labels=dict(score="auc"),
            color="model",
            color_discrete_map=model_colors,
        )

        fig.add_hline(
            THRESHOLD_LOW,
            line_dash="dash",
            line=dict(color=THRESHOLD_LOW_COLOR, width=2),
        )
        fig.add_hline(
            THRESHOLD_MID,
            line_dash="dash",
            line=dict(color=THRESHOLD_MID_COLOR, width=2),
        )

        fig.update_yaxes(range=[0, 1], fixedrange=True)
        fig.update_xaxes(fixedrange=True, tickangle=60, dtick="M5")

        return fig

    @output
    @render_plotly_streaming(recreate_key=filtered_model_names)
    def plot_dist():
        fig = px.histogram(
            filtered_df(),
            facet_row="model",
            nbins=20,
            x="score",
            labels=dict(score="auc"),
            color="model",
            color_discrete_map=model_colors,
        )

        fig.add_vline(
            THRESHOLD_LOW,
            line_dash="dash",
            line=dict(color=THRESHOLD_LOW_COLOR, width=2),
        )
        fig.add_vline(
            THRESHOLD_MID,
            line_dash="dash",
            line=dict(color=THRESHOLD_MID_COLOR, width=2),
        )

        # From https://plotly.com/python/facet-plots/#customizing-subplot-figure-titles
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

        fig.update_yaxes(matches=None)
        fig.update_xaxes(range=[0, 1], fixedrange=True)
        fig.layout.height = 500

        return fig


app = App(app_ui, server)
