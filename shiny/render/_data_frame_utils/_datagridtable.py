from __future__ import annotations

# TODO-barret-future; make DataTable and DataGrid generic? By currently accepting `object`, it is difficult to capture the generic type of the data.
import abc
import json
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Protocol,
    TypeVar,
    Union,
    overload,
    runtime_checkable,
)

from htmltools import HTML, MetadataNode, Tagifiable, TagNode

from ..._docstring import add_example, no_example
from ..._typing_extensions import TypedDict
from ...session import Session
from ...session._utils import RenderedDeps, require_active_session
from ...types import Jsonifiable
from ._selection import (
    RowSelectionModeDeprecated,
    SelectionModeInput,
    SelectionModes,
    as_selection_modes,
)
from ._unsafe import serialize_numpy_dtypes

if TYPE_CHECKING:
    import pandas as pd

    DataFrameT = TypeVar("DataFrameT", bound=pd.DataFrame)
    # TODO-future; Pandas, Polars, api compat, etc.; Today, we only support Pandas

    DataFrameResult = Union[
        None,
        pd.DataFrame,
        "DataGrid",
        "DataTable",
    ]
else:
    # The parent class of `data_frame` needs something to hold onto
    # To avoid loading pandas, we use `object` as a placeholder
    DataFrameResult = Union[None, object, "DataGrid", "DataTable"]


class AbstractTabularData(abc.ABC):
    @abc.abstractmethod
    def to_payload(self) -> dict[str, Jsonifiable]: ...


def as_editable(
    editable: bool,
    *,
    name: str,
) -> bool:
    editable = bool(editable)
    if editable:
        print(
            f"`{name}(editable=true)` is an experimental feature. "
            "If you find any bugs or would like different behavior, "
            "please make an issue at https://github.com/posit-dev/py-shiny/issues/new"
        )
    return editable


@add_example(ex_dir="../../api-examples/data_frame")
class DataGrid(AbstractTabularData):
    """
    Holds the data and options for a :class:`~shiny.render.data_frame` output, for a
    spreadsheet-like view.

    Parameters
    ----------
    data
        A pandas `DataFrame` object, or any object that has a `.to_pandas()` method
        (e.g., a Polars data frame or Arrow table).
    width
        A _maximum_ amount of horizontal space for the data grid to occupy, in CSS units
        (e.g. `"400px"`) or as a number, which will be interpreted as pixels. The
        default is `fit-content`, which sets the grid's width according to its contents.
        Set this to `100%` to use the maximum available horizontal space.
    height
        A _maximum_ amount of vertical space for the data grid to occupy, in CSS units
        (e.g. `"400px"`) or as a number, which will be interpreted as pixels. If there
        are more rows than can fit in this space, the grid will scroll. Set the height
        to `"auto"` to allow the grid to grow to fit all of the rows (this is not
        recommended for large data sets, as it may crash the browser).
    summary
        If `True` (the default), shows a message like "Viewing rows 1 through 10 of 20"
        below the grid when not all of the rows are being shown. If `False`, the message
        is not displayed. You can also specify a string template to customize the
        message, containing `{start}`, `{end}`, and `{total}` tokens. For example:
        `"Viendo filas {start} a {end} de {total}"`.
    filters
        If `True`, shows a row of filter inputs below the headers, one for each column.
    editable
        If `True`, allows the user to edit the cells in the grid. When a cell is edited,
        the new value is sent to the server for processing. The server can then return
        a new value for the cell, which will be displayed in the grid.
    html_columns
    selection_mode
        Single string or a `set`/`list`/`tuple` of string values to define possible ways
        to select data within the data frame.

        Supported values:
        * Use `"none"` to disable any cell selections or editing.
        * Use `"row"` to allow a single row to be selected at a time.
        * Use `"rows"` to allow multiple rows to be selected by clicking on them
        individually.

        Resolution rules:
        * If `"none"` is supplied, all other values will be ignored.
        * If both `"row"` and `"rows"` are supplied, `"row"` will be dropped (supporting `"rows"`).
    row_selection_mode
        Deprecated. Please use `mode={row_selection_mode}_row` instead.

    Returns
    -------
    :
        An object suitable for being returned from a `@render.data_frame`-decorated
        output function.

    See Also
    --------
    * :func:`~shiny.ui.output_data_frame`
    * :class:`~shiny.render.data_frame`
    * :class:`~shiny.render.DataTable`
    """

    data: pd.DataFrame
    width: str | float | None
    height: str | float | None
    summary: bool | str
    filters: bool
    editable: bool
    selection_modes: SelectionModes
    html_columns: tuple[int, ...] | Literal["auto"]

    def __init__(
        self,
        data: pd.DataFrame | PandasCompatible,
        *,
        width: str | float | None = "fit-content",
        height: str | float | None = None,
        summary: bool | str = True,
        filters: bool = False,
        editable: bool = False,
        selection_mode: SelectionModeInput = "none",
        html_columns: (
            Literal["auto"] | bool | int | list[int] | tuple[int, ...]
        ) = "auto",
        row_selection_mode: RowSelectionModeDeprecated = "deprecated",
    ):

        self.data = cast_to_pandas(
            data,
            "The DataGrid() constructor didn't expect a 'data' argument of type",
        )

        self.width = width
        self.height = height
        self.summary = summary
        self.filters = filters
        self.editable = as_editable(editable, name="DataGrid")
        self.selection_modes = as_selection_modes(
            selection_mode,
            name="DataGrid",
            editable=self.editable,
            row_selection_mode=row_selection_mode,
        )
        self.html_columns = as_html_columns(html_columns, self.data)

    def to_payload(self) -> dict[str, Jsonifiable]:
        res, html_columns = serialize_pandas_df(
            self.data, html_columns=self.html_columns
        )
        res["options"] = dict(
            width=self.width,
            height=self.height,
            summary=self.summary,
            filters=self.filters,
            editable=self.editable,
            htmlColumns=html_columns,
            style="grid",
            fill=self.height is None,
        )
        return res


def as_html_columns(
    html_columns: Literal["auto"] | bool | int | list[int] | tuple[int, ...],
    data: pd.DataFrame,
) -> tuple[int, ...] | Literal["auto"]:
    if html_columns == "auto":
        return "auto"

    if html_columns is False:
        return tuple[int]([])

    if html_columns is True:
        return tuple(range(len(data.columns)))

    if isinstance(html_columns, int):
        return (html_columns,)

    if isinstance(html_columns, (list, tuple)):

        for col in html_columns:
            if not isinstance(col, int):
                raise TypeError(
                    f"`html_columns=` expected an int or a list/tuple of ints, but found '{type(col)}'."
                )
        return tuple(html_columns)

    raise TypeError(
        f"The `html_columns=` expected a bool, int, or a list/tuple of ints, but found '{type(html_columns)}'."
    )


@no_example()
class DataTable(AbstractTabularData):
    """
    Holds the data and options for a :class:`~shiny.render.data_frame` output, for a
    spreadsheet-like view.

    Parameters
    ----------
    data
        A pandas `DataFrame` object, or any object that has a `.to_pandas()` method
        (e.g., a Polars data frame or Arrow table).
    width
        A _maximum_ amount of vertical space for the data table to occupy, in CSS units
        (e.g. `"400px"`) or as a number, which will be interpreted as pixels. The
        default is `fit-content`, which sets the table's width according to its
        contents. Set this to `100%` to use the maximum available horizontal space.
    height
        A _maximum_ amount of vertical space for the data table to occupy, in CSS units
        (e.g. `"400px"`) or as a number, which will be interpreted as pixels. If there
        are more rows than can fit in this space, the table body will scroll. Set the
        height to `None` to allow the table to grow to fit all of the rows (this is not
        recommended for large data sets, as it may crash the browser).
    summary
        If `True` (the default), shows a message like "Viewing rows 1 through 10 of 20"
        below the grid when not all of the rows are being shown. If `False`, the message
        is not displayed. You can also specify a string template to customize the
        message, containing `{start}`, `{end}`, and `{total}` tokens. For example:
        `"Viendo filas {start} a {end} de {total}"`.
    filters
        If `True`, shows a row of filter inputs below the headers, one for each column.
    editable
        If `True`, allows the user to edit the cells in the grid. When a cell is edited,
        the new value is sent to the server for processing. The server can then return
        a new value for the cell, which will be displayed in the grid.
    selection_mode
        Single string or a `set`/`list`/`tuple` of string values to define possible ways
        to select data within the data frame.

        Supported values:
        * Use `"none"` to disable any cell selections or editing.
        * Use `"row"` to allow a single row to be selected at a time.
        * Use `"rows"` to allow multiple rows to be selected by clicking on them
        individually.

        Resolution rules:
        * If `"none"` is supplied, all other values will be ignored.
        * If both `"row"` and `"rows"` are supplied, `"row"` will be dropped (supporting `"rows"`).
    row_selection_mode
        Deprecated. Please use `mode={row_selection_mode}_row` instead.

    Returns
    -------
    :
        An object suitable for being returned from a `@render.data_frame`-decorated
        output function.

    See Also
    --------
    * :func:`~shiny.ui.output_data_frame`
    * :class:`~shiny.render.data_frame`
    * :class:`~shiny.render.DataGrid`
    """

    data: pd.DataFrame
    width: str | float | None
    height: str | float | None
    summary: bool | str
    filters: bool
    selection_modes: SelectionModes
    html_columns: tuple[int, ...] | Literal["auto"]

    def __init__(
        self,
        data: pd.DataFrame | PandasCompatible,
        *,
        width: str | float | None = "fit-content",
        height: str | float | None = "500px",
        summary: bool | str = True,
        filters: bool = False,
        editable: bool = False,
        selection_mode: SelectionModeInput = "none",
        html_columns: (
            Literal["auto"] | bool | int | list[int] | tuple[int, ...]
        ) = "auto",
        row_selection_mode: Literal["deprecated"] = "deprecated",
    ):

        self.data = cast_to_pandas(
            data,
            "The DataTable() constructor didn't expect a 'data' argument of type",
        )

        self.width = width
        self.height = height
        self.summary = summary
        self.filters = filters
        self.editable = as_editable(editable, name="DataTable")
        self.selection_modes = as_selection_modes(
            selection_mode,
            name="DataTable",
            editable=self.editable,
            row_selection_mode=row_selection_mode,
        )
        self.html_columns = as_html_columns(html_columns, self.data)

    def to_payload(self) -> dict[str, Jsonifiable]:
        res, html_columns = serialize_pandas_df(
            self.data, html_columns=self.html_columns
        )
        res["options"] = dict(
            width=self.width,
            height=self.height,
            summary=self.summary,
            filters=self.filters,
            editable=self.editable,
            htmlColumns=html_columns,
            style="table",
        )
        return res


def serialize_pandas_df(
    df: "pd.DataFrame",
    *,
    html_columns: tuple[int, ...] | Literal["auto"],
) -> tuple[dict[str, Any], tuple[int, ...]]:

    columns = df.columns.tolist()
    columns_set = set(columns)
    if len(columns_set) != len(columns):
        raise ValueError(
            "The column names of the pandas DataFrame are not unique."
            " This is not supported by the data_frame renderer."
        )

    # Currently, we don't make use of the index; drop it so we don't error trying to
    # serialize it or something
    df = df.reset_index(drop=True)

    # # Can we keep the original column information?
    # # Maybe we need to inspect the original columns for any "unknown" column type. See if it contains any HTML or Tag objects
    # for col in columns:
    #     if df[col].dtype.name == "unknown":
    #         print(df[col].to_list())
    #         raise ValueError(
    #             "The pandas DataFrame contains columns of type 'object'."
    #             " This is not supported by the data_frame renderer."
    #         )

    type_hints = serialize_numpy_dtypes(df)

    if html_columns == "auto":
        html_columns_set = set[int]()
        for i, type_hint in zip(range(len(columns)), type_hints):
            if type_hint["type"] == "unknown":
                # Go through column values and check if they contain py-htmltools objects
                for val in df[  # pyright: ignore[reportUnknownVariableType]
                    columns[i]
                ].to_list():
                    if isinstance(val, (HTML, Tagifiable, MetadataNode)):
                        # If they do, mark the column and extra htmldeps
                        html_columns_set.add(i)
                        break

        ret_html_columns = tuple(html_columns_set)
    else:
        ret_html_columns = html_columns
    # print(ret_html_columns)

    if len(ret_html_columns) > 0:
        # Enable copy-on-write mode for the data;
        # Use `deep=False` to avoid copying the full data; CoW will copy the necessary data when modified
        import pandas as pd

        with pd.option_context("mode.copy_on_write", True):
            df = df.copy(deep=False)
            session = require_active_session(None)

            def wrap_shiny_html_with_session(x: TagNode) -> CellHtml:
                return wrap_shiny_html(x, session=session)

            for html_column in ret_html_columns:
                df[df.columns[html_column]] = df[
                    df.columns[html_column]
                ].apply(  # pyright: ignore[reportUnknownMemberType]
                    wrap_shiny_html_with_session
                )

    def handle_html(x: Any) -> str | float | bool | list[Any] | dict[Any, Any]:
        if isinstance(x, (HTML, Tagifiable, MetadataNode)):
            raise ValueError(
                "Please set `DataGrid(html_columns='auto')` or DataTable(html_columns='auto')` to enable HTML for all columns. Found a `TagNode` within a cell."
            )
        return x

    res = json.loads(
        # {index: [index], columns: [columns], data: [values]}
        df.to_json(  # pyright: ignore[reportUnknownMemberType]
            None,
            orient="split",
            default_handler=handle_html,
        )
    )

    res["typeHints"] = type_hints

    print(json.dumps(res, indent=4))

    return (res, ret_html_columns)


@runtime_checkable
class PandasCompatible(Protocol):
    # Signature doesn't matter, runtime_checkable won't look at it anyway
    def to_pandas(self) -> pd.DataFrame: ...


@overload
def cast_to_pandas(x: DataFrameT, error_message_begin: str) -> DataFrameT: ...


@overload
def cast_to_pandas(x: PandasCompatible, error_message_begin: str) -> pd.DataFrame: ...


def cast_to_pandas(
    x: DataFrameT | PandasCompatible, error_message_begin: str
) -> DataFrameT | pd.DataFrame:
    import pandas as pd

    if isinstance(x, pd.DataFrame):
        return x

    if isinstance(x, PandasCompatible):
        return x.to_pandas()

    raise TypeError(
        error_message_begin
        + f" '{str(type(x))}'. Use either a pandas.DataFrame, or an object"
        " that has a .to_pandas() method."
    )


class CellHtml(TypedDict):
    isShinyHtml: bool
    obj: RenderedDeps


@overload
def wrap_shiny_html(x: TagNode, *, session: Session) -> CellHtml: ...
@overload
def wrap_shiny_html(x: Jsonifiable, *, session: Session) -> Jsonifiable: ...
def wrap_shiny_html(
    x: Jsonifiable | TagNode, *, session: Session
) -> Jsonifiable | CellHtml:
    print("\n\n")
    print("wrap_shiny_html", x)
    if not isinstance(x, (HTML, Tagifiable)):
        if isinstance(x, (str, int, float, bool, list, dict, tuple)):
            return x
    print("wrap_shiny_html2", x)
    html_and_deps = session._process_ui(x)
    return {"isShinyHtml": True, "obj": html_and_deps}
