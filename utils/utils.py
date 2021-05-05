import datetime

from flask_login import current_user


def get_message_from_form(form):
    for i in form.__dict__.values():
        if hasattr(i, 'errors'):
            if i.errors:
                msg = f'{i.label.text}: {i.errors[0]}'
                return msg
    return ''


def get_duration_from_time(time):
    duration = datetime.datetime.combine(
        datetime.date.min, time) - datetime.datetime.min
    return duration


def date_format():
    return '%d %B %Y, %H:%M'
