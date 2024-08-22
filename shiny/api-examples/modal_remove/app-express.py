from shiny import reactive
from shiny.express import input, ui


def run_model(delay=10.0):
    import time

    # Pretend to run a model for `delay` seconds
    start_time = time.time()
    while time.time() - start_time < delay:
        pass
    return time.time()


ui.input_action_button("run", "Run Model")

model_result = reactive.value()


def the_modal():
    return ui.modal(
        "The model is running, please wait.",
        title="Running model",
        easy_close=False,
        footer=None,
    )


@reactive.effect
@reactive.event(input.run)
def do_run_model():
    # Show the modal, blocking interaction with the UI
    ui.modal_show(the_modal())

    result = run_model(delay=2)

    # Now that we have model results, remove the modal
    # and update the model result reactive value
    ui.modal_remove()
    model_result.set(result)
