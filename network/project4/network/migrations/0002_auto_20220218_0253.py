# Generated by Django 3.2.3 on 2022-02-18 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='age',
        ),
        migrations.RemoveField(
            model_name='user',
            name='bio',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(default='Edit Bio Here', max_length=500),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birth_date',
            field=models.DateField(blank=True, default='Enter Birthdate here', null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='location',
            field=models.CharField(blank=True, default='Location you live?', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(default='Name Edit Here', max_length=30),
        ),
    ]
