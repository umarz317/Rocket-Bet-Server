# Generated by Django 4.0.4 on 2022-08-26 19:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server_api', '0005_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='expiry',
            field=models.IntegerField(default=1661541285.7279842),
        ),
        migrations.AlterField(
            model_name='session',
            name='token',
            field=models.CharField(max_length=32, validators=[django.core.validators.MinLengthValidator(12, 'Invalid Length!')]),
        ),
    ]
