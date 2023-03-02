import argparse
import os
from datetime import date, timedelta

from jinja2 import Environment, FileSystemLoader

from src.io.reader.fee_reader import read_fees
from src.io.reader.mandate_reader import read_mandates
from src.io.reader.member_reader import read_members
from src.model.bill import Bill, Position
from src.routines.routine import Routine
from src.utils.format import format_currency, format_date


class FeeMailsPrepareRoutine(Routine):

    def get_name(self) -> str:
        return 'fee_mails_prepare'
    
    def get_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'workbook',
            help='The excel workbook containing the member, payment and SEPA mandate data.\nAllowed file formats: [.xls, xlsx, .xlsm, .xslb].'
        )
        parser.add_argument(
            '-o',
            '--outdir',
            default='./out',
            help='The output directory for the generated html messages.'
        )
        parser.add_argument(
            '-t',
            '--template',
            default='/fee_mails/message.html.jinja',
            help='The path to the message template file relative to the templates/ folder.\nAllowed file formats: [.html, .jinja, .html.jinja].'
        )
        parser.add_argument(
            '-v',
            '--value-date',
            default=date.today() + timedelta(weeks=2),
            help='The date on which the payments will be collected. It must be at least two (2) weeks in advance.'
        )
        parser.add_argument(
            '-u',
            '--update-date',
            default=date.today() + timedelta(weeks=1),
            help='The deadline for members to update their personal data or bank details. Should be at most one (1) week before the value date.'
        )
        parser.add_argument(
            '-e',
            '--contact-email',
            default='schatzmeister@jubo.info',
            help='The e-mail adress of the person responsible for the membership fees and other questions.'
        )
        return parser

    def run(self, args: dict = {}):
        # Prepare the template engine environment (Jinja) and fetch the template
        print(f'Reading the template from {args.template}.')
        jinja_env = Environment(
            loader=FileSystemLoader('./templates')
        )
        jinja_env.globals['format_date'] = format_date
        jinja_env.globals['format_currency'] = format_currency
        template = jinja_env.get_template(args.template)  
        print(f'Template read successfully.')

        # Retrieve the data from the specified excel sheet
        print(f'Reading members, fees and mandates from {args.workbook}".')
        members = read_members(args.workbook, 'Mitglieder')
        fees = read_fees(args.workbook, 'Finanzen')
        mandates = read_mandates(args.workbook, 'Finanzen')
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
                payments[mandate.member_id]['mandate'] = mandate
        print(f'Paying members: {len(members)}.')

        # Prepare the bills
        print('Preparing the bills.')
        bills = []
        total_fees = 0.0
        total_donations = 0.0
        for payment in payments.values():
            positions = [
                Position(
                    description='Fee',
                    amount=payment['fee'].amount
                )
            ]
            if payment['fee'].donation > 0:
                positions.append(
                    Position(
                        description='Donation',
                        amount=payment['fee'].donation
                    )
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
            f'Total Fees: {format_currency(total_fees)}.'
            f' Donations: {format_currency(total_donations)}.'
            f' Total: {format_currency(total_fees + total_donations)}.'
        )

        # Prepare the message contents and write them
        print(f'Creating the fee notification messages.')
        messages = {}
        for bill in bills:
            name = f'notification_{bill.member.id}'
            message = template.render(
                bill=bill,
                update_date=args.update_date,
                contact_email=args.contact_email
            )
            messages[name] = message
        print(f'Created {len(messages)} messages successfully.')

        # Write the messages to the output directory
        outdir = os.path.join(
            args.outdir,
            date.today().strftime('%Y-%m-%d')
        ) 
        print(f'Writing messages to {outdir}.')
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        for name, message in messages.items():
            with open(os.path.join(outdir, f'{name}.html'), 'w', encoding='utf-8') as file:
                file.write(message)
        print('Messages wrote successfully.')

        print('Exiting.')