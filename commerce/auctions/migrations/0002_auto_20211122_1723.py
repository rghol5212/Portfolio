# Generated by Django 3.2.3 on 2021-11-22 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activelisting',
            name='createdby',
            field=models.CharField(blank=True, default=None, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='activelisting',
            name='is_sold',
            field=models.BooleanField(default=False),
        ),
    ]
