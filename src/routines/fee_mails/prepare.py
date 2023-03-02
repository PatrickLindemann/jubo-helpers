import argparse
import json
import os
from datetime import date, timedelta
from typing import List

from humps import camelize, decamelize
from jinja2 import Environment, FileSystemLoader

from src.io.reader.fee_reader import read_fees
from src.io.reader.mandate_reader import read_mandates
from src.io.reader.member_reader import read_members
from src.model.bill import Bill, Position
from src.routines.routine import Routine
from src.utils.format import format_currency, format_date


class FeeMailsPrepareRoutine(Routine):

    def get_name(self) -> str:
        return 'fee-mails-prepare'
    
    def get_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'workbook',
            type=str,
            help='The excel workbook containing the member, payment and SEPA mandate data.\nAllowed file formats: [.xls, xlsx, .xlsm, .xslb].'
        )
        parser.add_argument(
            '-o',
            '--outdir',
            type=str,
            default='./out/fee-notifications',
            help='The output directory for the generated html messages.'
        )
        parser.add_argument(
            '-c',
            '--config',
            default='./config.json',
            help='The path to the configuration file.\nAllowed file formats: [.json].'
        )
        parser.add_argument(
            '-t',
            '--template',
            type=str,
            default='/fee_mails/message.html.jinja',
            help='The path to the message template file relative to the templates/ folder.\nAllowed file formats: [.html, .jinja, .html.jinja].'
        )
        parser.add_argument(
            '-v',
            '--value-date',
            type=date.fromisoformat,
            default=date.today() + timedelta(weeks=2),
            help='The date on which the payments will be collected. It must be at least two (2) weeks in advance. Format: "yyyy-MM-dd".'
        )
        parser.add_argument(
            '-u',
            '--update-date',
            type=date.fromisoformat,
            default=date.today() + timedelta(weeks=1),
            help='The deadline for members to update their personal data or bank details. Should be at most one (1) week before the value date. Format: "yyyy-MM-dd".'
        )
        parser.add_argument(
            '-e',
            '--contact-email',
            type=str,
            default='schatzmeister@jubo.info',
            help='The e-mail adress of the person responsible for the membership fees and other questions.'
        )
        return parser

    def run(self, args: dict = {}):             
        # Read the config
        print(f'Reading configuration from { args.config }.')
        with open(args.config) as file:
            config = json.load(file)
        config = decamelize(config)
        print(
            f'Config read sucessfully.\n Contact: { config["signature"]["name"] }'\
            f' ({ config["signature"]["email"] })'
        )

        # Prepare the template engine environment (Jinja) and fetch the template
        print(f'Reading the template from {args.template}.')
        jinja_env = Environment(
            loader=FileSystemLoader('./templates'),
            trim_blocks=True,
            lstrip_blocks=True
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
        print(f'Paying members: {len(paying_members)}.')

        # Prepare the bills
        print('Preparing the bills.')
        bills: List[Bill] = []
        total_fees = 0.0
        total_donations = 0.0
        for payment in payments.values():
            positions = [
                Position(
                    description=f'Jahresbeitrag Mitgliedschaft ({ payment["member"].membership })<br/>'\
                                f'<small>Für den Zeitraum 01.01.{ (args.value_date.year) } - 31.12.{ args.value_date.year }</small>',
                    amount=payment['fee'].amount
                )
            ]
            if payment['fee'].donation > 0:
                positions.append(
                    Position(
                        description='Zusätzliche Spende',
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
        messages = []
        for bill in bills:
            metadata = {
                'file': f'notification_{bill.member.id}.html',
                'member': {
                    'id': bill.member.id,
                    'first_name': bill.member.first_name,
                    'last_name': bill.member.last_name,
                    'email': bill.member.email
                },
                'mandate': {
                    'reference': bill.mandate.reference
                }
            }
            content = template.render(
                bill=bill,
                update_date=args.update_date,
                contact_email=args.contact_email,
                signature=config['signature']
            )
            messages.append({ 'metadata': metadata, 'content': content })
        print(f'Created {len(messages)} messages successfully.')

        outdir = os.path.join(
            args.outdir,
            date.today().isoformat()
        )
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        # Write metadata to the output directory
        metadata_path = os.path.join(outdir, 'metadata.json')
        print(f'Writing metadata to {metadata_path}.')
        metadata = {
            'created_at': date.today().isoformat(),
            'contact_email': args.contact_email,
            'value_date': args.value_date.isoformat(),
            'update_date': args.update_date.isoformat(),
            'messages': [
                message['metadata'] for message in messages
            ],
            'total': len(messages),
        }
        with open(metadata_path, 'w', encoding='utf-8') as file:
            json.dump(camelize(metadata), file, indent=4)
        print(f'Metadata wrote successfully.')

        # Write the messages to the output directory
        print(f'Writing messages to {outdir}.')
        for message in messages:
            with open(
                os.path.join(outdir, message['metadata']['file']),
                'w',
                encoding='utf-8'
            ) as file:
                file.write(message['content'])
        print('Messages wrote successfully.')

        print('Exiting.')