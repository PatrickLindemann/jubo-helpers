from model.bill import Bill
from reader.reader import read_excel

'''
Constants
'''

SHEET = 'Beiträge'

ATTRIBUTE_MAP = {
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

'''
Functions
'''

def read_bills(file):
    data = read_excel(file, SHEET, ATTRIBUTE_MAP)
    bills = list(map(lambda x: Bill(**x), data))
    return bills