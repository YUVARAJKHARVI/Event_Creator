# Generated by Django 3.2.7 on 2021-12-09 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0004_events_list'),
    ]

    operations = [
        migrations.DeleteModel(
            name='events_list',
        ),
    ]