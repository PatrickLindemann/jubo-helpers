from datetime import date


def format_currency(value: float) -> str:
    return '{:,.2f}€'.format(value)

def format_date(value: date) -> str:
    return value.strftime('%d.%m.%Y')

def format_time(value: date) -> str:
    return value.strftime('%H:%M:%S')

def format_datetime(value: date) -> str:
    return value.strftime('%d.%m.%Y %H:%M:%S')