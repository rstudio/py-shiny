from typing import Optional

from shiny import App, Inputs, Outputs, Session, ui
from shiny.render._render import RendererMeta, renderer_gen


@renderer_gen
def render_test_text(
    meta: RendererMeta,
    value: str | None,
    *,
    extra_txt: Optional[str] = None,
) -> str | None:
    if value is None:
        return None
    value = str(value)
    value += "; "
    value += "async" if meta["is_async"] else "sync"
    if extra_txt:
        value = value + "; " + str(extra_txt)
    return value


app_ui = ui.page_fluid(
    ui.code("t1:"),
    ui.output_text_verbatim("t1"),
    ui.code("t2:"),
    ui.output_text_verbatim("t2"),
    ui.code("t3:"),
    ui.output_text_verbatim("t3"),
    ui.code("t4:"),
    ui.output_text_verbatim("t4"),
    ui.code("t5:"),
    ui.output_text_verbatim("t5"),
    ui.code("t6:"),
    ui.output_text_verbatim("t6"),
)


def server(input: Inputs, output: Outputs, session: Session):
    @output
    @render_test_text
    def t1():
        return "t1; no call"
        # return "hello"

    @output
    @render_test_text
    async def t2():
        return "t2; no call"

    @output
    @render_test_text()
    def t3():
        return "t3; call"

    @output
    @render_test_text()
    async def t4():
        return "t4; call"

    @output
    @render_test_text(extra_txt="w/ extra_txt")
    def t5():
        return "t5; call"

    @output
    @render_test_text(extra_txt="w/ extra_txt")
    async def t6():
        return "t6; call"


app = App(app_ui, server)
