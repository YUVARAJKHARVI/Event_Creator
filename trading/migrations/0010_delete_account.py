# Generated by Django 3.2.7 on 2021-12-10 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0009_account_is_admin'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Account',
        ),
    ]
