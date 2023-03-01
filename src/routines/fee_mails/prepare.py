import argparse
import locale
from datetime import date, timedelta
from os import path

from jinja2 import Environment

from src.io.reader.fee_reader import read_fees
from src.io.reader.mandate_reader import read_mandates
from src.io.reader.member_reader import read_members
from src.model.bill import Bill, Position
from src.routines.routine import Routine


class FeeMailsPrepareRoutine(Routine):

    def get_name(self) -> str:
        return 'fee_mails_prepare'
    
    def get_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()
        parser.add_argument('input')
        parser.add_argument('outdir', default='./data/messages/') #TODO:
        parser.add_argument('value_date', default=date.today() + timedelta(weeks=2))
        parser.add_argument('update_date', default=date.today() + timedelta(weeks=1))
        parser.add_argument('contact_email', default='schatzmeister@jubo.info')
        parser.add_argument('template_path', default='./templates/fee_notification.html.jinja')
        return parser

    def print_payments(self, payments: dict):
        headers = [
            'ID',
            'First Name',
            'Last Name',
            'E-Mail',
            'Status',
            'Fee',
            'Donation',
            'Total'
        ]
        rows = []
        for payment in payments.values():
            member = payment['member']
            bill = payment['bill']
            rows.append([
                member.id,
                member.first_name,
                member.last_name,
                member.email,
                member.membership,
                locale.currency(bill.fee),
                locale.currency(bill.donation),
                locale.currency(bill.total)
            ])
        table = [headers] + rows
        for row in table:
            print('{} {: >25} {: >25} {: >30} {: >10} {: >10} {: >10} {: >10}'.format(*row))

    def run(self, args: dict = {}):
        # Prepare the template engine environment (Jinja) and fetch the template
        locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8') 
        jinja_env = Environment(gobals={ 'locale': locale })
        print(f'Reading the template from {args.template_path}.')
        template = jinja_env.get_template()  
        print(f'Template read successfully.')

        # Retrieve the data from the specified excel sheet
        print(f'Reading members, fees and mandates from {args.input}".')
        members = read_members(args.input, 'Mitglieder')
        fees = read_fees(args.input, 'Beiträge')
        mandates = read_mandates(args.input, 'Beiträge')
        print(f'Data read successfully. Total members: {len(members)}.')

        # Filter paying members and add the fee and mandate details
        print('Filtering paying members and collecting payment info.')
        paying_members = list(
            filter(lambda m: m.status in ['Aktiv', 'Passiv', 'Inaktiv'], members)
        )
        payments = { member.id: { 'member': member } for member in paying_members }
        for fee in fees:
            if fee.member_id in payments:
                payments[fee.member_id]['fee'] = fee
        for mandate in mandates:
            if mandate.member_id in payments:
                mandates[mandate.member_id]['mandate'] = mandate
        print(f'Paying members: {len(members)}.')

        # Prepare the bills
        print('Preparing the bills.')
        bills = []
        total_fees = 0.0
        total_donations = 0.0
        for payment in payment.values():
            positions = [
                Position(description='Fee', amount=payment['fee'])
            ]
            if payment['donation'] > 0:
                positions.append(
                    Position(description='Donation', amount=payment['donation'])
                )
            bills.append(
                Bill(
                    member=payment['member'],
                    mandate=payment['mandate'],
                    positions=positions,
                    creation_date=date.today(),
                    value_date=args.value_date
                )
            )
            total_fees += payment['fee'].amount
            total_donations += payment['fee'].donation
        print(
            f'Total Fees: {locale.currency(total_fees)}.'
            f' Donations: {locale.currency(total_donations)}.'
            f' Total: {locale.currency(total_fees + total_donations)}.'
        )

        # Prepare the message contents and write them
        print(f'Creating the fee notification messages.')
        messages = {}
        for bill in bills:
            name = f'message_{bill.member.id}'
            message = template.render(
                bill=bill,
                update_date=args.update_date,
                contact_email=args.contact_email
            )
            messages[name] = message
        print(f'Created {len(messages)} successfully.')

        # Write the messages to the output directory
        outdir = path.join(args.outdir, date.today()) 
        print(f'Writing messages to {outdir}.')
        for name, message in messages.items():
            with open(path.join(outdir, name), 'w') as file:
                file.write(message)
        print('Messages wrote successfully.')

        print('Exiting.')