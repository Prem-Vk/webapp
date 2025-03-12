from candidate.models import Candidate
from rest_framework import serializers


class CandidateSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'age', 'gender', 'email', 'phone_number']

class CandidateSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['name']