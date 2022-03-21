from src.model.member import Member
from src.io.reader.excel_reader import read_excel

'''
Constants
'''

SHEET = 'Mitglieder'

ATTRIBUTE_MAP = {
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

'''
Functions
'''

def read_members(file_path):
    data = read_excel(file_path, SHEET, ATTRIBUTE_MAP)
    members = list(map(lambda x: Member(**x), data))
    return members