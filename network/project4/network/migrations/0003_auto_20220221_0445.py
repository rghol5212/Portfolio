# Generated by Django 3.2.3 on 2022-02-21 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_auto_20220218_0253'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='followers',
            new_name='following',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birth_date',
            field=models.DateField(blank=True, default='1900-01-01', null=True),
        ),
    ]