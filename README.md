# JuBO Helpers <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->
- [Pre-Requisites](#pre-requisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Fee Notification E-Mails](#fee-notification-e-mails)
    - [Configuration Setup](#configuration-setup)
    - [Prepare Notification E-Mails](#prepare-notification-e-mails)
      - [Parameters](#parameters)
    - [Send Notification E-Mail](#send-notification-e-mail)
      - [Parameters](#parameters-1)
- [Built With](#built-with)
- [Authors](#authors)

## Pre-Requisites

This project requires [Python](https://python.org) with minimum version 3.8. You can download and install it from the [official download page](https://www.python.org/downloads/). Afterwards, you can verify your installation in the terminal with the commands

```
python3 --version
```

and

```
pip --version
```

## Installation

First, clone this project through `git clone`. Then, navigate into the project's root folder and install the dependencies through [pip](https://pip.pypa.io/en/stable) with

```
pip install -r requirements.txt
```

## Usage

This section introduces the features of this project and explains their use-cases and usage.

### Fee Notification E-Mails

Once a year, the JuBO collects membership fees from its members. This is done through *SEPA direct debit mandates*(Lastschriftmandate). These payments must be announced to the members at least two (2) weeks before the debit collection day.

In order to automate this, the `fee-mail` pipeline provides methods to create and send these notification e-mails. After they are sent as, the debit collection itself is performed with the banking system.

#### Configuration Setup

Before usage, you need to configure the signature and e-mail servers in the `config.json` file.

Create a copy of the provided example configuration with

```
cp config.example.json config.json
```

Now, you can edit the newly created `config.json` and replace the example values with the real data. The file `schemas/config.schema.json` provides a JSON schema for your convenience.

#### Prepare Notification E-Mails

First, you need to prepare the e-mails with the member data provided in the member sheet of the JuBO (found in `Mitglieder/JuBO-Mitgliederliste.xlsx` in OneDrive).

Generate the e-mail messages with 

```
python3 helpers.py fee-mails-prepare <path/to/members.xlsx> [...parameters]
```

By default, the generated HTML messages will be written into the `out/` directory, together with a `metadata.json` file that contains the metadata for the messages.

To verify that the e-mails were generated correctly, you can open them locally with your browser.

##### Parameters

| Parameter | Shorthand | Description | Type | Default Value | Annotation(s) |
|---|---|---|---|---|---|
| --outdir | -o | The output directory for the generated html messages | string | `./out/` | |
| --config | -c | The path to the configuration file. | string | `./config.json` | Allowed file formats: `.json` |
| --template | -t | The path to the message template file relative to the `templates/` foldersc | string | `./fee-mails/message.html.jinja`  | Allowed file formats: `.html`, `.jinja`, `.html.jinja` |
| --value-date | -v | The date on which the payments will be collected. It must be at least two (2) weeks in advance. | date | *today + 14 days* | Date format: `yyyy-MM-dd` |
| --update-date | -u | The deadline for members to update their personal data or bank details. Should be at most one (1) week before the value date. | date | *today + 7 days* | Date format: `yyyy-MM-dd` |
| --contact-email | -e | desc | string | schatzmeister@jubo.info | |

#### Send Notification E-Mail

After you have generated and validated the notification messages, you can use the `fee-mails-send` command to send these e-mails to the members:

```
python3 helpers.py fee-mails-send <path/to/message-dir> [...parameters]
```

Before the e-mails are sent, you will be asked for confirmation. If you enter `y`, the e-mails are sent via the SMTP protocol by the user `mailServer.smtp.user` in the `config.json`.

##### Parameters

| Parameter | Shorthand | Description | Type | Default Value | Annotation(s) |
|---|---|---|---|---|---|
| --config | -c | The path to the configuration file. | string | `./config.json` | Allowed file formats: `.json` |

## Built With

- **[Pandas](https://pandas.pydata.org)** - A flexible and powerful data analysis / manipulation library for Python - [GitHub](https://github.com/pandas-dev/pandas)
- **[Jinja](https://jinja.palletsprojects.com)** - A very fast and expressive template engine for Python - [GitHub](https://github.com/pallets/jinja)

## Authors

- **Patrick Lindemann** - Initial work - [E-Mail](mailto:patrick.lindemann.99@gmail.com), [GitHub](https://github.com/PatrickLindemann)