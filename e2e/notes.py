"""Barret Facade classes for working with Shiny inputs/outputs in Playwright"""

# pyright: reportUnknownMemberType=false





from playwright.sync_api import Page


def test_barret_numeric(page: Page, app: ShinyAppProc) -> None:
    page.goto(app.url)

    obs = NumericInputJoe(page, "obs", wait=1000)
    # obs.wait_for(timeout = wait)

    obs.data.set_value(3)
    obs.set_value(3)

    obs.loc_root
    obs.loc
    obs.value = 3
    with timeout:
        obs.value = 3
    obs.set_value(3, timeout=1000)

    obs.wait_for(timeout=100)
    obs.value = 3

    obs.wait(timeout=1000)
    obs.value = 3

    other_obj.value = "bar"
    assert obs.value == "foo"

    other_obj.value = "bar2"
    other_obj.set_value("bar2", timeout)
    obs.expect.to_be_equal("foo2")
    assert obs.value == "foo2"

    # expect_obs = obs.expect
    # expect_obs.to_have_value("10")

    # Do not use `wait`, the `timeout` should be utilized for each command
    # Should there be multiple timeout values? - no. Confusion is not worth it, can use `with timeout` if needed

    # Call `.verify()` on init.
    # * Ideally, it'd be on first use of a locator

    obs = NumericInputJoe(page, "obs", verify=True, timeout=3000)

    obs.loc_root
    obs.loc
    # obs.value = 3

    # Expectation
    # Short-hand for:
    # obs.expect = expect(obs.loc)

    # Locations
    # Return a `Locator` object
    obs.loc
    obs.container
    # # obs.locs.default
    # # obs.locs.container
    # obs.locs.label
    # obs.locs.slider
    # obs.locs.start
    # # expect(obs.container).to_have_class("shiny-input-container")

    # # Default value
    # obs.value # 2
    # obs.value = 3
    # # Don't do this
    # obs.value = (3, field = "abcd")

    # Prolly what will happen in real life
    # obs.value # 2
    obs.move_slider(0.5)

    # No; Not this API approach
    # obs.get_value() # Do not encourage `get_*()` methods
    # Try to mirror playwright as much as possible.
    # There are no properties, only methods; (Locators will stay as properties)
    obs.fill(3, "abcd")
    # obs.loc.fill(3, "abcd")

    # !!! Don't sub-class. For now, use `_` separatation and use `loc` or `value` as a prefix
    obs.loc_start
    obs.value_start

    # # Supplement values...
    # obs.values.start
    # obs.values.end

    # Supplement objects
    # No setter field methods
    obs.date_start
    obs.start  # ?
    obs.date_end
    obs.end  # ?

    # Methods
    # Try to use the "active bindings" approach
    obs.slider = 0.45
    obs.move_slider()

    ## Timeouts
    # Timeout is None everywhere
    # Override with `page_timeout(page, timeout)` or `page.set_default_timeout(timeout)`

    # Local timeout
    obs = NumericInputJoe(page, "obs", timeout=None)

    # Global timeout
    # Can you have a field and a method with the same name?
    with page_timeout(page, 6 * 1000):
        obs.value = 3

    # Assertions
    expect(obs.loc).to_have_value("3")

    obs.set_value(3)
    # Can not use `assert` methods as it needs to wait for the next value
    assert obs.value == 3, "object equals 3"
