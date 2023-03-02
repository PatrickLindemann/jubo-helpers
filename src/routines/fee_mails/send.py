import argparse
import json
import os
from datetime import date

from humps import decamelize

from src.mail.client import EmailClientWithSSL, EmailClientWithSSLConfig
from src.model.mail import Mail
from src.routines.routine import Routine


class FeeMailsSendRoutine(Routine):

    def get_name(self) -> str:
        return 'fee-mails-send'
    
    def get_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'indir',
            help='The input directory containing fee notification e-mail message(s) and metadata.json.'
        )
        parser.add_argument(
            '-c',
            '--config',
            default='./config.json',
            help='The path to the configuration file.'
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

        # Read the metadata
        metadata_path = os.path.join(args.indir, 'metadata.json')
        print(f'Reading message metadata from {metadata_path}.')
        with open(metadata_path, 'r', encoding='utf-8') as file:
            metadata = json.load(file)
        metadata = decamelize(metadata)
        print('Metadata read successfully.')

        # Read the messages
        print(f'Reading messages from {args.indir}.')
        messages = []
        for message_metadata in metadata['messages']:
            file_path = os.path.join(args.indir, message_metadata['file'])
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            messages.append({
                'metadata': message_metadata,
                'content': content
            })
        assert(len(messages) == metadata['total'])
        print(f'Read {len(messages)} message(s) successfully.')        

        # TODO: Signature

        # Prepare the e-mails
        mails = []
        sender = config['mail_server']['smtp']['user']
        for message in messages:
            member = message['metadata']['member']
            year = date.fromisoformat(metadata['value_date']).year
            mails.append(
                Mail(
                    sender=sender,
                    recipients=member['email'],
                    subject=f'JuBO e.V. | Mitgliedsbeitrag { year } | Mitglied Nr. M{ member["id"] } { member["first_name"] } { member["last_name"] }',
                    body=message['content']
                )
            )

        client = EmailClientWithSSL(
            imap=config['mail_server']['imap'],
            smtp=config['mail_server']['smtp']
        )

        # Ask for confirmation
        confirm = input(
            f'Send email(s) with sender address {sender}? [y/N]'
        )
        if confirm.lower() != 'y':
            print('Exiting.')
            exit()

        for mail in mails:
            print(f'Sending email to { mail.recipients }.')
            client.send(mail)
        client.close()
        print(f'Sent { len(mails) } e-mail message(s) successfully.')

        print('Exiting.')