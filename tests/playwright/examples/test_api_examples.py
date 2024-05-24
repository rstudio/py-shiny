import pytest
from example_apps import get_apps, reruns, reruns_delay, validate_example

from shiny.test import Page


@pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
@pytest.mark.parametrize("ex_app_path", get_apps("shiny/api-examples"))
def test_api_examples(page: Page, ex_app_path: str) -> None:
    validate_example(page, ex_app_path)
