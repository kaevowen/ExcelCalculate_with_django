from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=20)
    user_email = models.EmailField(unique=True)
    user_pw = models.CharField(max_length=100)
    user_validate = models.BooleanField(default=False)