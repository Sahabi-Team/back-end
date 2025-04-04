from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class UserPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    """Generates a token for password reset"""
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)

password_reset_token = UserPasswordResetTokenGenerator()
