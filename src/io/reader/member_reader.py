from typing import List

from src.io.reader.excel_reader import read_excel
from src.model.member import Member

MEMBER_HEADERS = {
    'ID': 'id',
    'Anrede': 'salutation',
    'Vorname': 'first_name',
    'Nachname': 'last_name',
    'Straße': 'street',
    'HausNr.': 'house_number',
    'PLZ': 'zip_code',
    'Ort': 'city',
    'E-Mail': 'email',
    'Festnetz': 'phone_fixed',
    'Mobil': 'phone_mobile',
    'Geburtsdatum': 'birth_date',
    'Alter': 'age',
    'Status': 'status',
    'Mitgliedschaft': 'membership',
    'Rolle': 'role',
    'Position': 'position',
    'Beitrittsdatum': 'join_date',
    'Austrittsdatum': 'exit_date',
    'Tätigkeit': 'occupation',
    'Anmerkung(en)': 'comment'
}

def read_members(
        workbook_path: str,
        sheet_name: str
) -> List[Member]:
    """ Read member data from an excel sheet.

    Parameters
    ----------
    workbook_path : str
        The file path to the excel workbook
    sheet_name : str
        The name of the member worksheet

    Returns
    -------
    list[Member]
        The list of member objects
    """
    df = read_excel(workbook_path, sheet_name, MEMBER_HEADERS)
    return list(map(lambda x: Member(**x), df.to_dict(orient='records')))