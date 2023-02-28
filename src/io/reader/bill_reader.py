from typing import List
from src.model.bill import Bill
from src.io.reader.excel_reader import read_excel

BILL_HEADER_MAP = {
    'MitgliedsNr.': 'member_id',
    'Vorname': 'first_name',
    'Nachname': 'last_name',
    'Straße': 'street',
    'HausNr.': 'house_number',
    'PLZ': 'zip_code',
    'Ort': 'city',
    'Beitrag': 'fee',
    'Spende': 'donation',
    'Summe': 'total', 
    'Letzte Zahlung': 'last_payment_date',
    'Gläubiger-ID': 'creditor_id',
    'Referenz': 'reference',
    'Erteilt Am': 'issue_date',
    'Kreditinstitut': 'credit_institute',
    'IBAN': 'iban',
    'BIC': 'bic'
}

def read_bills(
    workbook_path: str,
    sheet_name: str = 'Beiträge',
    header_map = BILL_HEADER_MAP
) -> List[Bill]:
    """_summary_

    Parameters
    ----------
    workbook_path : str
        The file path to the excel workbook
    sheet_name : str, optional
        The name of the worksheet, by default 'Beiträge'
    header_map : dict, optional
       The name mapping for headers. If a header is a key from the dict, it
       will be substituded by the respective value, by default BILL_HEADER_MAP

    Returns
    -------
    list[Bill]
        The list of bill objects
    """
    data = read_excel(workbook_path, sheet_name, header_map)
    bills = list(map(lambda x: Bill(**x), data))
    return bills