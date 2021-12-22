from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy


# Create your models here.
class User(AbstractUser):
    """
    Class for model of crm user, extands standdart django User with user_photo field
    """
    user_photo = models.ImageField(upload_to='user_photo/', default='user_photo/default.jpg')

    def get_manager_access(self):
        """
        Returns True if user is in Managers group or is Admin or is stuff.
        """
        return self.is_staff or self.groups.filter(name='Managers').exists()

    def get_user_naming(self):
        """
        Returns user's first_name and last name if defined, else returns username
        """
        if self.first_name and self.last_name:
            return self.get_full_name()
        else:
            return self.get_username()
