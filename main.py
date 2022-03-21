import argparse
import locale
from datetime import date, timedelta

from src.io.reader.bill_reader import read_bills
from src.io.reader.config_reader import read_config
from src.io.reader.member_reader import read_members
from src.io.remote.email_client import EmailClient
from src.model.mail import Mail

# Parse the arguments from the command line
parser = argparse.ArgumentParser()
parser.add_argument('input')
args = parser.parse_args()

# Read the config
config = read_config('./config.json')

# Get the current year
year = int(date.today().strftime("%Y"))

# Prepare the locale for euro currency formatting
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8') 

# Read the excel file with the email receipients
print(f'Reading members and bills from "{ args.input }".')
members = read_members(args.input)
bills = read_bills(args.input)
print(f'Members: { len(members) }')

# Filter active, passive and inactive members
ACTIVE_STATUSES = ('Aktiv', 'Passiv', 'Inaktiv')
print(f'Filtering payments with members that have the status { ACTIVE_STATUSES }.')
paying_members = list(filter(lambda m: m.status in ACTIVE_STATUSES, members))
paying_members = list(filter(lambda m: m.email != '-', paying_members)) #TODO remove
print(f'Payments: { len(paying_members) }')

# Link the billing information to the respective member
payments = { m.id: { 'member': m } for m in paying_members }
for bill in bills:
    if bill.member_id in payments:
        payments[bill.member_id]['bill'] = bill

# Print the list of payments and ask for confirmation
total = 0.0
table = [['ID', 'First Name', 'Last Name', 'E-Mail', 'Status', 'Fee', 'Donation', 'Total']]
for payment in payments.values():
    member = payment['member']
    bill = payment['bill']
    total += bill.total
    table.append([
        member.id,
        member.first_name,
        member.last_name,
        member.email,
        member.membership,
        locale.currency(bill.fee),
        locale.currency(bill.donation),
        locale.currency(bill.total)
    ])

for row in table:
    print('{} {: >25} {: >25} {: >30} {: >10} {: >10} {: >10} {: >10}'.format(*row))

print(f'Total amount: { locale.currency(total) }')
confirm = input('Send the messages? [y/N]')
if confirm.lower() != 'y':
    print('Exiting.')
    exit()

# Read the signature
with open('./templates/signature.html', 'r') as file:
    signature = file.read()

# Read the e-Mail style sheet
with open('./templates/styles.css', 'r') as file:
    styles = file.read()

print(f'Preparing { len(payments) } payment e-mails.')
mails = []
for payment in payments.values():
    member = payment['member']
    bill = payment['bill']
    # Prepare the e-mail message
    sender = config.user.email
    recipient = member.email
    subject = f'JuBO e.V. | Mitgliedsbeitrag { year } & Datenaktualisierung | Mitglied Nr. M{ member.id } { member.first_name } { member.last_name }'
    body = f'''
        <html>
            <head>
                <style>
                    { styles }
                </style>
            </head>
            <body>
                <p>
                    { 'Liebe' if member.salutation == 'Frau' else 'Lieber' } { member.first_name },
                </p>
                <p>
                    wie jedes Jahr um diese Zeit stehen die Mitgliedsbeiträge für die JuBO e.V. zur Zahlung an. Dein diesjähriger Beitrag setzt sich für Dich wie folgt zusammen:
                </p>
                <table id="payment-details">
                    <tr>
                        <th>Pos.</th>
                        <th>Beschreibung</th>
                        <th>Betrag</th>
                    </tr>
                    <tr>
                        <td>1</td>
                        <td>
                            Jahresbeitrag Mitgliedschaft ({ member.membership })<br/>
                            <small>Für den Zeitraum 01.01.{ (year - 1) } - 01.01.{ year }</small>
                        </td>
                        <td>{ locale.currency(bill.fee) }</td>
                    </tr>
                    <tr>
                        <td>2</td>
                        <td>Zusätzliche Spende</td>
                        <td>{ locale.currency(bill.donation) }</td>
                    </tr>
                    <tr class="total-row">
                        <td></td>
                        <td>Gesamtsumme</td>
                        <td>{ locale.currency(bill.total) }</td>
                    </tr>
                </table>
                <p>
                    Da Du uns freundlicherweise ein SEPA-Lastschriftmandat erteilt hast, werden wir den fälligen Betrag i.H.v. <b>{ locale.currency(bill.total) }</b> zum <b>31.03.2022</b> vom folgenden Konto
                    per SEPA-Lastschrift einziehen:
                </p>
                <table id="bank-details">
                    <tr>
                        <td>Kontoinhaber</td>
                        <td>{ bill.first_name } { bill.last_name }</td>
                    </tr>
                    <tr>
                        <td>IBAN (anonymisiert)</td>
                        <td>{ bill.anonymized_iban() }</td>
                    </tr>
                    <tr>
                        <td>BIC (anonymisiert)</td>
                        <td>{ bill.anonymized_bic() }</td>
                    </tr>
                </table>
                <p>
                    Du erkennst unsere Abbuchung an der Mandatsreferenz <i>{ bill.reference }</i> und Gläubiger-Identifikationsnummer <i>{ bill.creditor_id }</i>. Wir bitten um Kontodeckung zu sorgen.
                </p>
                <p>
                    <b>Wichtig:</b> Falls sich seit letztem Jahr Deine personenbezogenen Daten (Name, Adresse, E-Mail, Handynummer, etc.) geändert haben sollten, dann antworte
                    bitte auf diese E-Mail mit Deinen aktualisierten Daten. Sollten sich zusätzlich Deine Bankdaten geändert haben, dann füge Deiner Mail bitte ein neu
                    ausgefülltes Lastschriftmandat bei und sende es uns bis spätestens <b>27.03.2022</b> zu.
                </p>
                <p>
                    Falls Du noch Rückfragen zu Deiner Abbuchung oder Mitgliedschaft haben solltest, kannst Du Dich jederzeit über <a href="mailto:schatzmeister@jubo.info">schatzmeister@jubo.info</a> bei mir melden.
                </p>
                <p>
                    Vielen Dank, dass Du uns unterstützt!
                </p>
                <p>
                    { signature }
                </p>
                <p>   
                    <i>Bitte beachten: Dieses Schreiben wurde maschinell erzeugt und ist ohne Unterschrift gültig.</i>
                </p>
            </body>
        </html>
    '''
    mails.append(Mail(sender, recipient, subject, body))

client = EmailClient(config)
for mail in mails:
    print(f'Sending message to { mail.recipients }')
    client.send(mail)
client.close()
print(f'Sent { len(mails) } e-mail message(s) successfully.')