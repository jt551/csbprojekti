# Generated by Django 3.1.2 on 2020-12-26 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flawedapp', '0002_creditcards'),
    ]

    operations = [
        migrations.RenameField(
            model_name='creditcards',
            old_name='cvs',
            new_name='csc',
        ),
    ]
