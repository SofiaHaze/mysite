# ~/user/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.
class User(AbstractBaseUser):
    name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(verbose_name='email', max_length=100, blank=True, null=True, unique=True)
    user_id = models.CharField(max_length=30, blank=True, null=True)
    profile_image = models.TextField(blank=True, null=True)  # 프로필 이미지
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['user_id']

    def __str__(self):
        return self.user_id

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = 'users'
