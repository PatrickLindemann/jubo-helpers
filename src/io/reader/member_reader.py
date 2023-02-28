from typing import List
from src.model.member import Member
from src.io.reader.excel_reader import read_excel

MEMBER_HEADER_MAP = {
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
        sheet_name: str = 'Mitglieder',
        header_map: dict = MEMBER_HEADER_MAP
) -> List[Member]:
    """ Read member data from an excel sheets and retrieve a list of Member
    dataclass objects.

    Parameters
    ----------
    workbook_path : str
        The file path to the excel workbook
    sheet_name : str, optional
        The name of the worksheet, by default 'Mitglieder'
    header_map : dict, optional
        The name mapping for headers. If a header is a key from the dict, it
        will be substituded by the respective value, by default MEMBER_HEADER_MAP

    Returns
    -------
    list[Member]
        The list of member objects
    """
    data = read_excel(workbook_path, sheet_name, header_map)
    members = list(map(lambda x: Member(**x), data))
    return members