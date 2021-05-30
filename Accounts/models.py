from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
	#いいね総数
	good_points = models.IntegerField()
	#所属学部、学科
	belong = models.CharField(max_length=100)
	#称号
	degree = models.CharField(max_length=100, blank=True, null=True)
	#ユーザー画像
	image = models.ImageField(upload_to='', blank=True, null=True)

	class Meta:
		verbose_name='CustomUser'