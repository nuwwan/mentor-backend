from django.core.exceptions import ValidationError


def no_spaces_validator(value):
    if " " in value:
        raise ValidationError("Text field cannot contain spaces.")
