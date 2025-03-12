import re
from django.core.exceptions import ValidationError

def phone_number_validator(number):
    if not re.match('^[0-9]{10}$', str(number)):
        raise ValidationError('Phone Number Invalid')