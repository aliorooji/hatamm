from django.db import models

# Create your models here.
from django.utils import timezone


class TelegramUser(models.Model):
    pass


class InterestedOptions(models.Model):
    pass


class RegisteredByTelegram(models.Model):
    pass


class Reports(models.Model):
    chat_id = models.CharField(max_length=20)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)