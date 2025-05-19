# dump_utf8.py
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sahabi.settings')  
django.setup()

from django.core.management import call_command

with io.open('db.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', indent=2, stdout=f)
