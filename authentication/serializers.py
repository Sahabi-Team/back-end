from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from .utils import password_reset_token
from rest_framework.exceptions import ValidationError
from client_auth.models import Trainee
from trainer_auth.models import Trainer
from sahabi.settings import PRODUCTION_DOMAIN
class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()

    def get_profile_picture(self, obj):
        return f"{PRODUCTION_DOMAIN}{obj.profile_picture.url}" if obj.profile_picture else None

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'profile_picture')

class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=["trainee", "trainer"], write_only=True)  # Accept only "trainee" or "trainer"

    class Meta:
        model = User
        fields = ["id", "name", "username", "email", "password", "phone_number", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        role = validated_data.pop("role")
        validated_data["usertype"]=role
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)

        if role == "trainee":
            Trainee.objects.create(user=user)
        elif role == "trainer":
            Trainer.objects.create(user=user)

        return user


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Check if the new password and confirm password match."""
        if data['new_password'] != data['confirm_password']:
            raise ValidationError("The new passwords do not match.")
        
        try:
            validate_password(data['new_password'])  # Ensure the new password is valid
        except ValidationError as e:
            raise ValidationError({"new_password": list(e.messages)})
        
        return data

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """Check if email exists in the database"""
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No account found with this email.")
        return value

    def save(self):
        """Generate token and send reset link via email"""
        email = self.validated_data["email"]
        user = User.objects.get(email=email)
        token = password_reset_token.make_token(user)

        # Generate Password Reset Link with just the token
        reset_link = f"{PRODUCTION_DOMAIN}/reset-password/{token}/"

        # Send Email
        send_mail(
            subject="Password Reset Request",
            message=f"Click the link below to reset your password:\n{reset_link}",
            from_email="mohammadhosseinpanbechi8908@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    def validate(self, data):
        """Validate the token and email combination"""
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise ValidationError("Invalid email address.")

        if not password_reset_token.check_token(user, data['token']):
            raise ValidationError("Invalid or expired token.")

        # Validate the new password
        try:
            validate_password(data['new_password'])
        except ValidationError as e:
            raise ValidationError({"new_password": list(e.messages)})

        return data

    def save(self):
        """Reset the user's password"""
        user = User.objects.get(email=self.validated_data['email'])
        user.set_password(self.validated_data['new_password'])
        user.save()

class ProfilePictureSerializer(serializers.Serializer):
    profile_picture = serializers.ImageField()

# class PasswordResetRequestSerializer(serializers.Serializer):
#     email = serializers.EmailField()

#     def validate(self, attrs):
#         email = attrs.get('email')
#         if not User.objects.filter(email=email).exists():
#             raise serializers.ValidationError("User with this email does not exist.")
#         return attrs

# class PasswordResetConfirmSerializer(serializers.Serializer):
#     uidb64 = serializers.CharField()
#     token = serializers.CharField()
#     new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     confirm_password = serializers.CharField(write_only=True, required=True)

#     def validate(self, attrs):
#         try:
#             uid = smart_str(urlsafe_base64_decode(attrs.get('uidb64')))
#             user = User.objects.get(id=uid)
#         except (User.DoesNotExist, DjangoUnicodeDecodeError):
#             raise serializers.ValidationError("Invalid token or user ID.")

#         if not PasswordResetTokenGenerator().check_token(user, attrs.get('token')):
#             raise serializers.ValidationError("Invalid or expired token.")

#         if attrs.get('new_password') != attrs.get('confirm_password'):
#             raise serializers.ValidationError("Passwords do not match.")

#         return attrs

#     def save(self):
#         uid = smart_str(urlsafe_base64_decode(self.validated_data['uidb64']))
#         user = User.objects.get(id=uid)
#         user.set_password(self.validated_data['new_password'])
#         user.save()
