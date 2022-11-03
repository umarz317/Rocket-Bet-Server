import time

from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator

from . import validators


class User(models.Model):
    pid = models.AutoField(primary_key=True)
    wallet_address = models.CharField(max_length=42, validators=[MinLengthValidator(int(42), "Address incorrect")],
                                      null=False)
    user_email = models.CharField(max_length=200,
                                  validators=[
                                      RegexValidator('([\\w]+[.s-]{0,1})+@[A-Za-z]*(.com)', 'Email not correct!')],
                                  null=False, unique=True)
    user_name = models.CharField(max_length=200,null=False,unique=True)
    password = models.CharField(max_length=200, validators=[
        MinLengthValidator(int(6), "Password should be a minimum of 6 characters"), validators.PasswordValidator],
                                null=False)
    is_active = models.BooleanField(default=False)
    avatar = models.IntegerField(default=0)

    def __str__(self):
        return self.wallet_address


class Auth(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.IntegerField(validators=[MinLengthValidator(6, "Invalid Length!")])
    expiry = models.IntegerField(null=True)


class Session(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=32, validators=[MinLengthValidator(12, "Invalid Length!")])
    expiry = models.FloatField(default=time.time() + (60 * 10))


class Chips(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    chips_count = models.IntegerField(default=0, null=False)
