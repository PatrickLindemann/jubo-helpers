from typing import List

from src.io.reader.excel_reader import read_excel
from src.model.mandate import Mandate

MANDATE_HEADER_MAP = {
    'MitgliedsNr.': 'member_id',
    'Vorname': 'first_name',
    'Nachname': 'last_name',
    'Straße': 'street',
    'HausNr.': 'house_number',
    'PLZ': 'zip_code',
    'Ort': 'city',
    'Gläubiger-ID': 'creditor_id',
    'Referenz': 'reference',
    'Erteilt Am': 'issue_date',
    'Kontoinhaber': 'account_owner',
    'IBAN': 'iban',
    'BIC': 'bic',
    'Kreditinstitut': 'credit_institute'
}

def read_mandates(
    workbook_path: str,
    sheet_name: str
) -> List[Mandate]:
    """ Read SEPA mandate data from an excel sheet.

    Parameters
    ----------
    workbook_path : str
        The file path to the excel workbook
    sheet_name : str, optional
        The name of the mandate worksheet

    Returns
    -------
    list[Mandate]
        The list of mandate objects
    """
    data = read_excel(workbook_path, sheet_name, MANDATE_HEADER_MAP)
    mandate = list(map(lambda x: Mandate(**x), data))
    return mandate