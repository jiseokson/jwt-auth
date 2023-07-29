import re
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from accounts.models import TRACK

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ['password', 'groups', 'user_permissions',]

    def validate_phone(self, data):
        if not re.match(r'^010-\d{4}-\d{4}$', data):
            raise ValidationError('Invalid phone number')
        return data
    
    def validate_track(self, data):
        if data not in TRACK:
            raise ValidationError('Invalid track name')
        return data
    
    def validate_student_id(self, data):
        if not re.match(r'^[a-zA-Z]\d{6}$', data):
            raise ValidationError('Invalid student ID')
        return data
    