import { ResponseValue, makeRequest } from "./request";

import { CellState } from "./cell";

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
  id: string;
  cellInfos: UpdateCellData[];
  onSuccess: (values: ResponseValue[]) => void;
  onError: (err: string) => void;
  columns: readonly string[];
  setData: (fn: (draft: unknown[][]) => void) => void;
  setCellEditMap: (
    fn: (draft: Map<string, { value: string; state: CellState }>) => void
  ) => void;
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
    "outputRPC",
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
          const key = `[${rowIndex}, ${columnIndex}]`;

          const obj =
            draft.get(key) ?? ({} as { value: string; state: CellState });
          obj.value = value;
          obj.state = CellState.EditSuccess;
          // console.log("Setting cell edit map");
          draft.set(key, obj);
        });
      });
      onSuccess(values);
    },
    (err: string) => {
      onError(err);
    },
    undefined
  );
}
