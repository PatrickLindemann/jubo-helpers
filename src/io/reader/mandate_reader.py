from typing import List

from src.io.reader.excel_reader import read_excel
from src.model.mandate import Mandate

MANDATE_HEADERS = {
    'Referenz': 'id',
    'MitgliedsNr.': 'member_id',
    'Vorname': 'first_name',
    'Nachname': 'last_name',
    'Straße': 'street',
    'HausNr.': 'house_number',
    'PLZ': 'zip_code',
    'Ort': 'city',
    'Gläubiger-ID': 'creditor_id',
    'Erteilt Am': 'issue_date',
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
    df = read_excel(workbook_path, sheet_name, MANDATE_HEADERS)
    df['id'] = df['id'].fillna(0).astype(int).astype(str)
    df['iban'] = df['iban'].str.replace(' ', '')
    return list(map(lambda x: Mandate(**x), df.to_dict(orient='records')))