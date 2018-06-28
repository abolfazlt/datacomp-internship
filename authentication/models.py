import uuid

from django.contrib.auth.models import User
from django.db import models


class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='user')
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, db_index=True, verbose_name='uuid')
    active = models.BooleanField(default=False, verbose_name='active')
