from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy


# Create your models here.


class User(AbstractUser):
    user_photo = models.ImageField(upload_to='user_photo/', default='user_photo/default.jpg')

    def get_absolute_url(self):
        """
        Returns the url to access a particular profile instance.
        """
        return reverse_lazy('crmuser-cabinet', args=[self.name])
