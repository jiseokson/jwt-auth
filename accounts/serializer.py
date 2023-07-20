import re
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from accounts.models import TRACK

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ['password', 'groups', 'user_permissions',]

    def validate(self, data):
        if not re.match(r'^010-\d{4}-\d{4}$', data.get('phone')):
            raise ValidationError('Invalid phone number')
        if data.get('track') not in TRACK:
            raise ValidationError('Invalid track name')
        if not re.match(r'^[a-zA-Z]\d{6}$', data.get('student_id')):
            raise ValidationError('Invalid student ID')
        return data