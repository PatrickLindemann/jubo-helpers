import argparse
import json

from src.mail.client import EmailClientWithSSL
from src.model.mail import Mail
from src.routines.routine import Routine


class FeeMailsSendRoutine(Routine):

    def get_name(self) -> str:
        return 'fee_mails_send'
    
    def get_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()
        parser.add_argument('input')
        parser.add_argument('config', default='./config.json')
        return parser

    def run(self, args: dict = {}):
        pass
        '''
        # Read the config
        print(f'Reading configuration from {args.config_path}.')
        with open(args.config_path) as file:
            config = json.load(file)
        print(
            f'Config read sucessfully.'
            f' Contact: {config.contact.email}'
            f' ({config.contact.email})'
        )

        # TODO: Read the messages

        # TODO: Prepare the signature and combine the messages

        # Ask for confirmation
        confirm = input(
            f'Send {len(mails)} messages with e-mail {args.contact.email}? [y/N]'
        )
        if confirm.lower() != 'y':
            print('Exiting.')
            exit()

        print(f'Preparing { len(payments) } payment e-mails.')
        mails = []
        for payment in payments.values():
            member = payment['member']
            bill = payment['bill']
            # Prepare the e-mail message
            sender = config.user.email
            recipient = member.email
            subject = f'JuBO e.V. | Mitgliedsbeitrag { year } & Datenaktualisierung | Mitglied Nr. M{ member.id } { member.first_name } { member.last_name }'
            mails.append(Mail(sender, recipient, subject, body))

        client = EmailClient(config)
        for mail in mails:
            print(f'Sending message to { mail.recipients }')
            client.send(mail)
        client.close()
        print(f'Sent { len(mails) } e-mail message(s) successfully.')
        '''