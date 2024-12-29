# profiles/signals.py
from django.db.backends.signals import connection_created
from django.db import connection

def enable_foreign_keys(sender, connection, **kwargs):
    if connection.vendor == 'sqlite':
        with connection.cursor() as cursor:
            cursor.execute('PRAGMA foreign_keys = ON;')

# Connect the signal to the connection_created event
connection_created.connect(enable_foreign_keys)
