import pathlib
import warnings

import pandas


def read_excel(
    workbook_path: pathlib.Path,
    sheet_name: str,
    header_map: dict = {},
    skip_rows: int = 0,
) -> pandas.DataFrame:
    """Read an Excel workbook into a DataFrame.

    Parameters
    ----------
    workbook_path : pathlib.Path
        The path to the Excel workbook.
    sheet_name : str
        The name of the sheet to read.
    header_map : dict, optional
        A mapping of the original column names to new column names, by default {}
    skip_rows : int, optional
        The number of rows to skip before reading the header, by default 0

    Returns
    -------
    pandas.DataFrame
        The DataFrame containing the data from the Excel workbook.
    """
    warnings.filterwarnings("ignore", module="openpyxl")
    df = pandas.read_excel(
        workbook_path,
        sheet_name=sheet_name,
        skiprows=max(0, skip_rows - 1),
    )
    df = df.drop(columns=[col for col in df if col not in header_map.keys()])
    df = df.rename(columns=header_map)
    warnings.filterwarnings("default", module="openpyxl")
    return df
