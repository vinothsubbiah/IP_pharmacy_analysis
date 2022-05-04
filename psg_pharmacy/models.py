from email import message
from django.db import models

# Create your models here.
class Messages(models.Model):
    message = models.CharField(max_length=50)
    from_user = models.CharField(max_length=30)
    to_user = models.CharField(max_length=30)

    def __str__(self):
        return self.message