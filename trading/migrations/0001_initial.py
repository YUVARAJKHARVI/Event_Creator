# Generated by Django 3.2.7 on 2021-11-12 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ideas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=255)),
                ('trade_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'ideas',
            },
        ),
    ]
