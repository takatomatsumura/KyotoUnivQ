from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):

	class Meta:
		verbose_name='CustomUser'