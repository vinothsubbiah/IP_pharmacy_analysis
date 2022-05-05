from email import message
from django.db import models

# Create your models here.
class Messages(models.Model):
    message = models.CharField(max_length=50)
    from_user = models.CharField(max_length=30)
    to_user = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class Mail(models.Model):
    message = models.CharField(max_length=200)
    from_user = models.CharField(max_length=30)
    to_user = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now_add=True)
