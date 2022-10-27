from django.core.exceptions import ValidationError
import re


def PasswordValidator(value):
    if value.islower():
        raise ValidationError("Password must contain an uppercase Character")
    if re.search(r'\d', value) is None:
        raise ValidationError("Password Must contain a number")
