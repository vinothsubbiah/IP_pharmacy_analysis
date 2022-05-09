from email import message
from django.db import models

# Create your models here.
class Messages(models.Model):
    message = models.CharField(max_length=1000)
    from_user = models.CharField(max_length=30)
    to_user = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class Mail(models.Model):
    # body = models.CharField(max_length=200)
    body = models.TextField(max_length=2000)
    from_user = models.CharField(max_length=30)
    to_user = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now_add=True)
