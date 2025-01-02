from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # If you want to extend the default Django User
    # or if you need something more advanced.
    # "AbstractUser" already has username, email, password, etc.
    is_admin = models.BooleanField(default=False)

    # Extra fields, if needed
    # e.g. profile_picture = models.ImageField(...)

    def __str__(self):
        return self.username
