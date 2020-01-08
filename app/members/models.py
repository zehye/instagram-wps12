from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    사용자 모델로 쓰입니다.
    """
    img_profile = models.ImageField('프로필이미지', blank=True, upload_to='users/')
    name = models.CharField('이름', max_length=30)


