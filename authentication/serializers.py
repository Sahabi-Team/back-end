from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from client_auth.models import Trainee
# from trainer.models import Trainer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number')

class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=["trainee", "trainer"], write_only=True)  # Accept only "trainee" or "trainer"

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "phone_number", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        role = validated_data.pop("role")
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)

        if role == "trainee":
            Trainee.objects.create(user=user)
        # elif role == "trainer":
        #     Trainer.objects.create(user=user)

        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        """Check if the old password matches the user's current password"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, data):
        """Check if the new password and confirm password match."""
        if data['new_password'] != data['confirm_password']:
            raise ValidationError("The new passwords do not match.")
        
        try:
            validate_password(data['new_password'])  # Ensure the new password is valid
        except ValidationError as e:
            raise ValidationError({"new_password": list(e.messages)})
        
        return data


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
