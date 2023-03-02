from typing import List

from src.io.reader.excel_reader import read_excel
from src.model.fee import Fee

FEE_HEADERS = {
    'MitgliedsNr.': 'member_id',
    'Beitrag': 'amount',
    'Spende': 'donation',
}

def read_fees(
    workbook_path: str,
    sheet_name: str
) -> List[Fee]:
    """ Read member fee data from an excel sheet.

    Parameters
    ----------
    workbook_path : str
        The file path to the excel workbook
    sheet_name : str, optional
        The name of the fee worksheet
    Returns
    -------
    list[Fee]
        The list of fee objects
    """
    df = read_excel(workbook_path, sheet_name, FEE_HEADERS)
    df[['amount', 'donation']] = df[['amount', 'donation']].fillna(0.0)
    return list(map(lambda x: Fee(**x), df.to_dict(orient='records')))