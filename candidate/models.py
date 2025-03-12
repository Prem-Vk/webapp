from django.db import models
from candidate.helpers import phone_number_validator

class Candidate(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    GENDERS = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Others')
    ]
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDERS)
    email = models.EmailField(unique=True)
    phone_number = models.BigIntegerField(validators=[phone_number_validator])

    def __str__(self):
        return f'{self.name}'
