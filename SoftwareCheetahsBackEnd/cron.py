import datetime

from villa.models import Calendar, Rule


def reminder_register():
    Rule.objects.create(text="salam")
