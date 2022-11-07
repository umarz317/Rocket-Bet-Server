from django.core.exceptions import ValidationError
import re


def PasswordValidator(value):
    if value.islower():
        raise ValidationError("Password must contain an uppercase Character")
    if re.search(r'\d', value) is None:
        raise ValidationError("Password Must contain a number")
    if re.search(r'\D', value) is None:
        raise ValidationError("Password Must contain a letter")


def LengthValidator(value):
    if len(value) < 6:
        raise ValidationError("Password Must contain a atleast 6 letters")
