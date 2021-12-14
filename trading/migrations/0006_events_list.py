# Generated by Django 3.2.7 on 2021-12-09 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0005_delete_events_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='events_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.CharField(default=0, max_length=255)),
            ],
            options={
                'db_table': 'events_list',
            },
        ),
    ]