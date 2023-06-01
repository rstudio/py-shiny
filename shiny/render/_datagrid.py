from __future__ import annotations

import abc
import json
import typing
from typing import Any, Awaitable, Callable, Literal, Optional, Union, cast, overload

from .. import _utils
from .._typing_extensions import Protocol, runtime_checkable
from ..render import RenderFunction, RenderFunctionAsync


class AbstractTabularData(abc.ABC):
    @abc.abstractmethod
    def to_payload(self) -> object:
        ...


class DataGrid(AbstractTabularData):
    def __init__(
        self,
        data: object,
        *,
        width: Union[str, float, None] = "fit-content",
        height: Union[str, float, None] = "500px",
        summary: Union[bool, str] = True,
        row_selection_mode: Union[
            Literal["none"], Literal["single"], Literal["multi-toggle"]
        ] = "none",
    ):
        """
        Holds the data and options for a ``shiny.render.data_grid`` output, for a
        spreadsheet-like view.

        Parameters
        ----------
        data
            A pandas `DataFrame` object, or any object that has a `.to_pandas()` method
            (e.g., a Polars data frame or Arrow table).
        width
            A width for the data grid to occupy, in CSS units. The default is `fit-content`,
            which sets the grid's width according to its contents. Set this to `100%` to use
            the maximum available horizontal space.
        height
            A _maximum_ amount of vertical space for the data grid to occupy, in CSS units.
            If there are more rows than can fit in this space, the grid will scroll.
        summary
            If `True` (the default), shows a message like "Viewing rows 1 through 10 of 20"
            below the grid when not all of the rows are being shown. If `False`, the message
            is not displayed. You can also specify a string template to customize the
            message, for example: `"Viendo filas {start} a {end} de {total}"`.
        row_selection_mode
            Use `"none"` to disable row selection, `"single"` to allow a single row to be
            selected at a time, and `"multi-toggle"` to allow multiple rows to be selected
            by clicking on them individually.

        Returns
        -------
        :
            An object suitable for being returned from a `@render.data_grid`-decorated
            output function.

        See Also
        --------
        ~shiny.ui.output_data_grid
        ~shiny.render.data_grid
        """
        import pandas as pd

        self.data: pd.DataFrame = cast(
            pd.DataFrame,
            cast_to_pandas(
                data,
                "The DataGrid() constructor didn't expect a 'data' argument of type",
            ),
        )

        self.width = width
        self.height = height
        self.summary = summary
        self.row_selection_mode = row_selection_mode

    def to_payload(self) -> object:
        res: dict[str, Any] = json.loads(
            # {index: [index], columns: [columns], data: [values]}
            self.data.to_json(  # pyright: ignore[reportUnknownMemberType]
                None, orient="split"
            )
        )
        res["options"] = dict(
            width=self.width,
            height=self.height,
            summary=self.summary,
            row_selection_mode=self.row_selection_mode,
            style="grid",
        )
        return res


class DataTable(AbstractTabularData):
    def __init__(
        self,
        data: object,
        *,
        width: Union[str, float, None] = "fit-content",
        height: Union[str, float, None] = "500px",
        summary: Union[bool, str] = True,
        row_selection_mode: Union[
            Literal["none"], Literal["single"], Literal["multi-toggle"]
        ] = "none",
    ):
        """
        Holds the data and options for a ``shiny.render.data_grid`` output, for a
        spreadsheet-like view.

        Parameters
        ----------
        data
            A pandas `DataFrame` object, or any object that has a `.to_pandas()` method
            (e.g., a Polars data frame or Arrow table).
        width
            A width for the data grid to occupy, in CSS units. The default is `fit-content`,
            which sets the grid's width according to its contents. Set this to `100%` to use
            the maximum available horizontal space.
        height
            A _maximum_ amount of vertical space for the data grid to occupy, in CSS units.
            If there are more rows than can fit in this space, the grid will scroll.
        summary
            If `True` (the default), shows a message like "Viewing rows 1 through 10 of 20"
            below the grid when not all of the rows are being shown. If `False`, the message
            is not displayed. You can also specify a string template to customize the
            message, for example: `"Viendo filas {start} a {end} de {total}"`.
        row_selection_mode
            Use `"none"` to disable row selection, `"single"` to allow a single row to be
            selected at a time, and `"multi-toggle"` to allow multiple rows to be selected
            by clicking on them individually.

        Returns
        -------
        :
            An object suitable for being returned from a `@render.data_grid`-decorated
            output function.

        See Also
        --------
        ~shiny.ui.output_data_grid
        ~shiny.render.data_grid
        """
        import pandas as pd

        self.data: pd.DataFrame = cast(
            pd.DataFrame,
            cast_to_pandas(
                data,
                "The DataGrid() constructor didn't expect a 'data' argument of type",
            ),
        )

        self.width = width
        self.height = height
        self.summary = summary
        self.row_selection_mode = row_selection_mode

    def to_payload(self) -> object:
        res: dict[str, Any] = json.loads(
            # {index: [index], columns: [columns], data: [values]}
            self.data.to_json(  # pyright: ignore[reportUnknownMemberType]
                None, orient="split"
            )
        )
        res["options"] = dict(
            width=self.width,
            height=self.height,
            summary=self.summary,
            row_selection_mode=self.row_selection_mode,
            style="table",
        )
        return res


# It would be nice to specify DataGridResult to be something like:
#   Union[pandas.DataFrame, <protocol with .to_pandas()>]
# However, if we did that, we'd have to import pandas at load time, which adds
# a nontrivial amount of overhead. So for now, we're just using `object`.
DataGridResult = Union[None, object, DataGrid]

RenderDataGridFunc = Callable[[], object]
RenderDataGridFuncAsync = Callable[[], Awaitable[object]]


@runtime_checkable
class PandasCompatible(Protocol):
    # Signature doesn't matter, runtime_checkable won't look at it anyway
    def to_pandas(self) -> object:
        ...


class RenderDataGrid(RenderFunction[DataGridResult, object]):
    def __init__(
        self,
        fn: RenderDataGridFunc,
    ) -> None:
        super().__init__(fn)
        # The Render*Async subclass will pass in an async function, but it tells the
        # static type checker that it's synchronous. wrap_async() is smart -- if is
        # passed an async function, it will not change it.
        self._fn: RenderDataGridFuncAsync = _utils.wrap_async(fn)

    def __call__(self) -> object:
        return _utils.run_coro_sync(self._run())

    async def _run(self) -> object:
        x = await self._fn()

        if x is None:
            return None

        if not isinstance(x, AbstractTabularData):
            x = DataGrid(
                cast_to_pandas(
                    x, "@render.data_grid doesn't know how to render objects of type"
                )
            )

        return x.to_payload()


def cast_to_pandas(x: object, error_message_begin: str) -> object:
    import pandas as pd

    if not isinstance(x, pd.DataFrame):
        if not isinstance(x, PandasCompatible):
            raise TypeError(
                error_message_begin
                + f" '{str(type(x))}'. Use either a pandas.DataFrame, or an object"
                " that has a .to_pandas() method."
            )
        return x.to_pandas()
    return x


class RenderDataGridAsync(RenderDataGrid, RenderFunctionAsync[DataGridResult, object]):
    def __init__(
        self,
        fn: RenderDataGridFuncAsync,
    ) -> None:
        if not _utils.is_async_callable(fn):
            raise TypeError(self.__class__.__name__ + " requires an async function")
        super().__init__(
            typing.cast(RenderDataGridFunc, fn),
        )

    async def __call__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
    ) -> object:
        return await self._run()


@overload
def data_grid(fn: RenderDataGridFunc | RenderDataGridFuncAsync) -> RenderDataGrid:
    ...


@overload
def data_grid() -> (
    Callable[[RenderDataGridFunc | RenderDataGridFuncAsync], RenderDataGrid]
):
    ...


def data_grid(
    fn: Optional[RenderDataGridFunc | RenderDataGridFuncAsync] = None,
) -> (
    RenderDataGrid
    | Callable[[RenderDataGridFunc | RenderDataGridFuncAsync], RenderDataGrid]
):
    """
    Reactively render a Pandas data frame object (or similar) as a basic HTML table.

    Parameters
    ----------
    index
        Whether to print index (row) labels.
    selection


    Returns
    -------
    :
        A decorator for a function that returns any of the following:

        1. A pandas :class:`DataFrame` object.
        2. A pandas :class:`Styler` object.
        3. Any object that has a `.to_pandas()` method (e.g., a Polars data frame or
           Arrow table).

    Tip
    ----
    This decorator should be applied **before** the ``@output`` decorator. Also, the
    name of the decorated function (or ``@output(id=...)``) should match the ``id`` of
    a :func:`~shiny.ui.output_table` container (see :func:`~shiny.ui.output_table` for
    example usage).

    See Also
    --------
    ~shiny.ui.output_data_grid
    """

    def wrapper(fn: RenderDataGridFunc | RenderDataGridFuncAsync) -> RenderDataGrid:
        if _utils.is_async_callable(fn):
            return RenderDataGridAsync(fn)
        else:
            return RenderDataGrid(fn)

    if fn is None:
        return wrapper
    else:
        return wrapper(fn)
