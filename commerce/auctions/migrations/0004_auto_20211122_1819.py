# Generated by Django 3.2.3 on 2021-11-22 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20211122_1729'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activelisting',
            name='is_sold',
        ),
        migrations.RemoveField(
            model_name='activelisting',
            name='upload_author',
        ),
    ]
