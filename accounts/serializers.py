from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .utils import verify_recaptcha

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    agree_to_terms = serializers.BooleanField(required=True)
    join_as_tasker = serializers.BooleanField(required=False)
    recaptcha_token = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        # Check terms
        if not data.get('agree_to_terms'):
            raise serializers.ValidationError({'agree_to_terms': 'You must agree to the terms.'})
        # Check reCAPTCHA
        token = data.get('recaptcha_token')
        if not verify_recaptcha(token):
            raise serializers.ValidationError({'recaptcha_token': 'Invalid reCAPTCHA. Please try again.'})
        return super().validate(data)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        data['join_as_tasker'] = self.validated_data.get('join_as_tasker', False)
        return data

    def save(self, request):
        user = super().save(request)
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.join_as_tasker = self.validated_data.get('join_as_tasker', False)
        user.save()
        return user