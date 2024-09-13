from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.


class User(AbstractUser):
    email = models.EmailField(verbose_name=_("email"),unique=True,max_length=100)



    def __str__(self):
        return f"User(id='{self.id}', email='{self.email}')"

