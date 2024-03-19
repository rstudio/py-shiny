import { ResponseValue, makeRequest } from "./request";

import type { CellState } from "./cell";
import { CellStateEnum } from "./cell";
import { CellEdit, SetCellEditMap, makeCellEditMapKey } from "./cell-edit-map";

export type UpdateCellData = {
  rowIndex: number;
  columnIndex: number;
  value: unknown;
  prev: unknown;
};
export type UpdateCellDataRequest = {
  row_index: number;
  column_index: number;
  value: unknown;
  prev: unknown;
};

export function updateCellsData({
  id,
  cellInfos,
  onSuccess,
  onError,
  columns,
  setData,
  setCellEditMap,
}: {
  id: string | null;
  cellInfos: UpdateCellData[];
  onSuccess: (values: ResponseValue[]) => void;
  onError: (err: string) => void;
  columns: readonly string[];
  setData: (fn: (draft: unknown[][]) => void) => void;
  setCellEditMap: SetCellEditMap;
}) {
  // // Skip page index reset until after next rerender
  // skipAutoResetPageIndex();

  const updateInfos: UpdateCellDataRequest[] = cellInfos.map((cellInfo) => {
    return {
      row_index: cellInfo.rowIndex,
      column_index: cellInfo.columnIndex,
      value: cellInfo.value,
      prev: cellInfo.prev,
    };
  });

  makeRequest(
    "output_handler",
    [
      // id: string
      id,
      // handler: string
      "cells_update",
      // list[OnCellUpdateParams]
      updateInfos,
    ],
    (values: ResponseValue[]) => {
      setData((draft) => {
        values.forEach((value: string, i: number) => {
          const { rowIndex, columnIndex } = cellInfos[i];
          draft[rowIndex][columnIndex] = value;
        });
      });
      setCellEditMap((draft) => {
        values.forEach((value: string, i: number) => {
          const { rowIndex, columnIndex } = cellInfos[i];

          const key = makeCellEditMapKey(rowIndex, columnIndex);
          const obj = draft.get(key) ?? ({} as CellEdit);
          obj.value = value;
          obj.state = CellStateEnum.EditSuccess;
          // Remove save_error if it exists
          delete obj.save_error;

          draft.set(key, obj);
        });
      });
      onSuccess(values);
    },
    (err: string) => {
      setCellEditMap((draft) => {
        cellInfos.forEach(({ rowIndex, columnIndex, value }) => {
          const key = makeCellEditMapKey(rowIndex, columnIndex);
          const obj = draft.get(key) ?? ({} as CellEdit);

          // Do not overwrite value!
          obj.value = String(value);

          obj.state = CellStateEnum.EditFailure;
          obj.save_error = String(err);
          // console.log("Setting cell edit map");
          draft.set(key, obj);
        });
      });
      onError(err);
    },
    undefined
  );
}
