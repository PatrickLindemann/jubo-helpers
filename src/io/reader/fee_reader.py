from typing import List

from src.io.reader.excel_reader import read_excel
from src.model.fee import Fee

FEE_HEADER_MAP = {
    'MitgliedsNr.': 'member_id',
    'Beitrag': 'fee',
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
    data = read_excel(workbook_path, sheet_name, FEE_HEADER_MAP)
    fee = list(map(lambda x: Fee(**x), data))
    return fee