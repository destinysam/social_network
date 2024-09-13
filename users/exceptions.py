from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed


class InvalidCredentials(AuthenticationFailed):
    default_detail = _("Invalid email or password")
