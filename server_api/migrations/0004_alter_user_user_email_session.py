# Generated by Django 4.0.4 on 2022-08-26 08:25

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server_api', '0003_remove_auth_hello'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_email',
            field=models.CharField(max_length=200, unique=True, validators=[django.core.validators.RegexValidator('([\\w]+[.-]{0,1})+@[A-Za-z]*(.com)', 'Email not correct!')]),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.IntegerField(validators=[django.core.validators.MinLengthValidator(12, 'Invalid Length!')])),
                ('expiry', models.IntegerField(default=600)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='server_api.user')),
            ],
        ),
    ]