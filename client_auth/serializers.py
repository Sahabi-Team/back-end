from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class ClientSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class ClientLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return attrs

class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        try:
            uid = smart_str(urlsafe_base64_decode(attrs.get('uidb64')))
            user = User.objects.get(id=uid)
        except (User.DoesNotExist, DjangoUnicodeDecodeError):
            raise serializers.ValidationError("Invalid token or user ID.")

        if not PasswordResetTokenGenerator().check_token(user, attrs.get('token')):
            raise serializers.ValidationError("Invalid or expired token.")

        if attrs.get('new_password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match.")

        return attrs

    def save(self):
        uid = smart_str(urlsafe_base64_decode(self.validated_data['uidb64']))
        user = User.objects.get(id=uid)
        user.set_password(self.validated_data['new_password'])
        user.save()
