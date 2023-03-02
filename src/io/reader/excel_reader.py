import warnings

import pandas as pd


def read_excel(
        workbook_path: str,
        sheet_name: str,
        header_map: dict = {},
        header_row: int = 4
) -> pd.DataFrame:
    """ Read data from an excel sheet into a DataFrame.

    Parameters
    ----------
    workbook_path : str
        The file path to the excel workbook
    sheet_name : str
        The name of the worksheet
    header_map : dict, optional
        The name mapping for headers. If a header is a key from the dict, it
        will be substituded by the respective value, by default {}
    header_row: int, optional
        The index of the header row for the worksheet, by default 4

    Returns
    -------
    pd.DataFrame
        The member data in a DataFrame
    """  
    warnings.filterwarnings('ignore', module='openpyxl')
    df = pd.read_excel(
        workbook_path,
        sheet_name=sheet_name,
        skiprows=max(0, header_row - 1),
    )
    df = df.drop(columns=[col for col in df if col not in header_map.keys()])
    df = df.rename(columns=header_map)
    warnings.filterwarnings('default', module='openpyxl')
    return df