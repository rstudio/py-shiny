from __future__ import annotations

from typing import Any, List, Tuple, TypedDict

import narwhals.stable.v1 as nw
import orjson
from htmltools import TagNode

from ..._typing_extensions import TypeIs
from ...session import require_active_session
from ._html import maybe_as_cell_html
from ._types import (
    CellPatch,
    CellValue,
    ColsList,
    DataFrame,
    DataFrameT,
    DType,
    FrameDtype,
    FrameJson,
    IntoDataFrame,
    IntoDataFrameT,
    PandasCompatible,
    RowsList,
)

__all__ = (
    "is_into_data_frame",
    "as_data_frame",
    "data_frame_to_native",
    "apply_frame_patches",
    "serialize_dtype",
    "serialize_frame",
    "subset_frame",
    "get_frame_cell",
    "frame_shape",
    "copy_frame",
    "frame_column_names",
)

########################################################################################
# Narwhals
#
# This module contains functions for working with data frames. It is a wrapper
# around the Narwhals library, which provides a unified interface for working with
# data frames (e.g. Pandas and Polars).
#
# The functions in this module are used to:
# * convert data frames to and from the Narwhals format,
# * apply patches to data frames,
# * serialize data frames to JSON,
# * subset data frames,
# * and get information about data frames (e.g. shape, column names).
#
# The functions in this module are used by the Shiny framework to work with data frames.
#
# For more information on the Narwhals library, see:
# * Intro https://narwhals-dev.github.io/narwhals/basics/dataframe/
# * `nw.DataFrame`: https://narwhals-dev.github.io/narwhals/api-reference/dataframe/
# * `nw.typing.IntoDataFrameT`: https://narwhals-dev.github.io/narwhals/api-reference/typing/#intodataframet
#
########################################################################################


# as_frame -----------------------------------------------------------------------------


def data_frame_to_native(data: DataFrame[IntoDataFrameT]) -> IntoDataFrameT:
    return nw.to_native(data)


def as_data_frame(
    data: IntoDataFrameT | DataFrame[IntoDataFrameT],
) -> DataFrame[IntoDataFrameT]:
    if isinstance(data, DataFrame):
        return data  # pyright: ignore[reportUnknownVariableType]
    try:
        return nw.from_native(data, eager_only=True)
    except TypeError as e:
        try:
            compatible_data = compatible_to_pandas(data)
            return nw.from_native(compatible_data, eager_only=True)
        except TypeError:
            # Couldn't convert to pandas, so raise the original error
            raise e


def compatible_to_pandas(
    data: IntoDataFrameT,
) -> IntoDataFrameT:
    """
    Convert data to pandas, if possible.

    Should only call this method if Narwhals can not handle the data directly.
    """
    # Legacy support for non-Pandas/Polars data frames that were previously supported
    # and converted to pandas
    if isinstance(data, PandasCompatible):
        from ..._deprecated import warn_deprecated

        warn_deprecated(
            "Returned data frame data values that are not Pandas or Polars `DataFrame`s are currently not supported. "
            "A `.to_pandas()` was found on your object and will be called. "
            "To remove this warning, please call `.to_pandas()` on your data "
            "and use the pandas result in your returned value. "
            "In the future, this will raise an error.",
            stacklevel=3,
        )
        return data.to_pandas()

    raise TypeError(f"Unsupported type: {type(data)}")


# TODO-future; Replace with `nw.is_into_data_frame(x)`?
def is_into_data_frame(
    data: IntoDataFrameT | object,
) -> TypeIs[IntoDataFrameT]:
    nw_df = nw.from_native(data, strict=False, eager_only=True)
    if isinstance(nw_df, nw.DataFrame):
        return True
    return False


# apply_frame_patches --------------------------------------------------------------------
def apply_frame_patches(
    nw_data: DataFrame[IntoDataFrameT],
    patches: List[CellPatch],
) -> DataFrame[IntoDataFrameT]:
    # data = data.clone()

    if len(patches) == 0:
        return nw_data

    # Apply the patches

    # TODO-future-barret; Might be faster to _always_ store the patches as a
    #     `cell_patches_by_column` object. Then iff they need the patches would we
    #     deconstruct them into a flattened list. Where as this conversion is being
    #     performed on every serialization of the data frame payload

    # # https://discord.com/channels/1235257048170762310/1235257049626181656/1283415086722977895
    # # Using narwhals >= v1.7.0
    # @nw.narwhalify
    # def func(df):
    #     return df.with_columns(
    #         df['a'].scatter([0, 1], [999, 888]),
    #         df['b'].scatter([0, 1], [777, 555]),
    #     )

    # Group patches by column
    # This allows for a single column to be updated in a single operation (rather than multiple updates to the same column)
    #
    # In; patches: List[Dict[row_index: int, column_index: int, value: Any]]
    # Out; cell_patches_by_column: Dict[column_name: str, List[Dict[row_index: int, value: Any]]]
    #
    cell_patches_by_column: dict[str, ScatterValues] = {}
    for cell_patch in patches:
        column_name = nw_data.columns[cell_patch["column_index"]]
        if column_name not in cell_patches_by_column:
            cell_patches_by_column[column_name] = {
                "row_indexes": [],
                "values": [],
            }

        # Append the row index and value to the column information
        cell_patches_by_column[column_name]["row_indexes"].append(
            cell_patch["row_index"]
        )
        cell_patches_by_column[column_name]["values"].append(cell_patch["value"])

    # Upgrade the Scatter info to new column Series objects
    scatter_columns = [
        nw_data[column_name].scatter(
            scatter_values["row_indexes"], scatter_values["values"]
        )
        for column_name, scatter_values in cell_patches_by_column.items()
    ]
    # Apply patches to the nw data
    return nw_data.with_columns(*scatter_columns)


# serialize_dtype ----------------------------------------------------------------------
nw_boolean = nw.Boolean()
nw_categorical = nw.Categorical()
nw_duration = nw.Duration()
nw_enum = nw.Enum()
nw_string = nw.String()
nw_date = nw.Date()
nw_datetime = nw.Datetime()
nw_object = nw.Object()


def serialize_dtype(col: nw.Series) -> FrameDtype:

    from ._html import series_contains_htmltoolslike

    dtype: DType = col.dtype

    if dtype == nw_string:
        type_ = "string"

    elif dtype.is_numeric():
        type_ = "numeric"

    elif dtype == nw_categorical:
        categories = col.cat.get_categories().to_list()
        return {"type": "categorical", "categories": categories}
    elif dtype == nw_enum:
        categories = col.cat.get_categories().to_list()
        return {"type": "categorical", "categories": categories}
    elif dtype == nw_boolean:
        type_ = "boolean"
    elif dtype == nw_date:
        type_ = "date"
    elif dtype == nw_datetime:
        type_ = "datetime"
    elif dtype == nw_duration:
        type_ = "duration"
    elif dtype == nw_object:
        type_ = "object"
        if series_contains_htmltoolslike(col):
            type_ = "html"

    else:
        type_ = "unknown"
        if series_contains_htmltoolslike(col):
            type_ = "html"

    return {"type": type_}


# serialize_frame ----------------------------------------------------------------------
def serialize_frame(into_data: IntoDataFrame) -> FrameJson:

    data = as_data_frame(into_data)

    type_hints = [serialize_dtype(data[col_name]) for col_name in data.columns]
    type_hints_type = [type_hint["type"] for type_hint in type_hints]

    data_rows = data.rows(named=False)

    # Shiny tag support
    if "html" in type_hints_type:
        session = require_active_session(None)

        def wrap_shiny_html_with_session(x: TagNode):
            return maybe_as_cell_html(x, session=session)

        html_column_positions = [
            i for i, x in enumerate(type_hints_type) if x == "html"
        ]

        new_rows: list[tuple[Any, ...]] = []

        # Wrap the corresponding columns with the cell html object
        for row in data_rows:
            new_row = list(row)
            for html_column_position in html_column_positions:
                new_row[html_column_position] = wrap_shiny_html_with_session(
                    new_row[html_column_position]
                )
            new_rows.append(tuple(new_row))

        data_rows = new_rows

    # _ = datetime(5)

    data_val = orjson.loads(
        orjson.dumps(
            data_rows,
            default=str,
            # option=(orjson.OPT_NAIVE_UTC),
        )
    )

    # import json
    # data_val = json.loads(json.dumps(data_rows, default=str))

    return {
        "columns": data.columns,
        "data": data_val,
        "typeHints": type_hints,
    }


# subset_frame -------------------------------------------------------------------------
def subset_frame(
    data: DataFrameT,
    *,
    rows: RowsList = None,
    cols: ColsList = None,
) -> DataFrameT:
    """Return a subsetted DataFrame, based on row positions and column names.

    Note that when None is passed, all rows or columns get included.
    """

    # Note that this type signature assumes column names are strings things.
    # This is always true in Polars, but not in Pandas (e.g. a column name could be an
    # int, or even a tuple of ints)
    if cols is None:
        if rows is None:
            return data
        else:
            # This feels like it should be `data[rows, :]` but that doesn't work for polars
            # https://github.com/narwhals-dev/narwhals/issues/989
            # Must use `list(rows)` as tuples are not supported
            # https://github.com/narwhals-dev/narwhals/issues/990
            return data[list(rows), data.columns]
    else:
        # `cols` is not None
        col_names = [data.columns[col] if isinstance(col, int) else col for col in cols]
        # If len(cols) == 0, then we should return an empty DataFrame
        # Currently this is broken when backed by pandas.
        # https://github.com/narwhals-dev/narwhals/issues/989
        if len(col_names) == 0:
            # Return a DataFrame with no rows or columns
            # If there are no columns, there are no Series objects to support any rows
            return data[[], []]

        if rows is None:
            return data[:, col_names]
        else:
            # Be sure rows is a list, not a tuple. Tuple
            return data[list(rows), col_names]


# # get_frame_cell -----------------------------------------------------------------------
def get_frame_cell(data: DataFrame[Any], row: int, col: int) -> Any:
    return data.item(row, col)


# shape --------------------------------------------------------------------------------
def frame_shape(data: IntoDataFrame) -> Tuple[int, int]:
    nw_data = as_data_frame(data)
    return nw_data.shape


def column_is_numeric(nw_data: DataFrame[Any], column_index: int) -> bool:
    series_dtype: DType = nw_data[:, column_index].dtype
    return series_dtype.is_numeric()


# copy_frame ---------------------------------------------------------------------------
def copy_frame(nw_data: DataFrameT) -> DataFrameT:
    return nw_data.clone()


# column_names -------------------------------------------------------------------------
def frame_column_names(into_data: IntoDataFrame) -> List[str]:
    return as_data_frame(into_data).columns


class ScatterValues(TypedDict):
    row_indexes: list[int]
    values: list[CellValue]
