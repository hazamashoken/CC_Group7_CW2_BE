import secrets
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


def _gen_token():
    """
    This is a function to generate a Bearer token
    """
    return secrets.token_urlsafe(64)


class AuthSession(models.Model):
    """
    This is a model for the user's Bearer token.
    :param user: The user's token.
    :param last_used: The last time the token was used.
    :param token: The token.
    :param TOKEN_TTL: The time to live of the token.
    :param is_verified_sms: Auth verified by SMS.
    :param is_verified_email: Auth verified by Email.
    :param is_verified_staff: Auth verified by human staff.
    """

    TOKEN_TTL = timedelta(days=1)  # 1 day

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    token = models.CharField(max_length=255, default=_gen_token)
    last_used = models.DateTimeField(auto_now=True)
    is_verified_sms = models.BooleanField(default=False)
    is_verified_email = models.BooleanField(default=False)
    is_verfied_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def refresh(self):
        """
        update last used
        """
        self.save()

    def regenerate(self):
        """
        Regenerates token without deleting the session.
        """
        self.token = _gen_token()
        self.save()

    @property
    def is_expired(self) -> bool:
        """
        Checks if token is expired.
        """
        return timezone.now() > self.last_used + self.TOKEN_TTL

    def expires_at(self) -> int:
        """
        Returns the expiry time of the token in Epoch
        """
        return int((self.last_used + self.TOKEN_TTL).timestamp())

    def __str__(self):
        return f"{self.user.email} : {self.expires_at()} : {self.token}"
