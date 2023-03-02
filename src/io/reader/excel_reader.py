import pandas as pd
import warnings

def read_excel(
        workbook_path: str,
        sheet_name: str, header_map: dict = {},
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
    # Read the workbook
    warnings.filterwarnings('ignore', module='openpyxl')
    df = pd.read_excel(workbook_path, sheet_name=sheet_name)
    # Replace invalid values (such as NaN) with None
    warnings.filterwarnings('default', module='openpyxl')
    df = df.replace({ pd.np.nan: None })
    # Retrieve the column header mapping
    headers = df.iloc[header_row - 2]
    keys = list(map(lambda x: header_map[x] if x in header_map else None, headers))
    # Read the table data
    result = []
    for j in range(header_row - 1, len(df)):
        row = df.iloc[j]
        entry = {}
        for i in range(len(row)):
            if keys[i]:
                entry[keys[i]] = row[i]
        result.append(entry)
    return result