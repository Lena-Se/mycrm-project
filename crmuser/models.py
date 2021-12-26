"""
This module contains model classes for crmuser application
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from crmuser.hashupload import OverwriteStorage, upload_func


class User(AbstractUser):
    """
    Class for model of crm user, extands standard django User with user_photo field
    """

    # user photo field
    user_photo = models.ImageField(upload_to=upload_func,  storage=OverwriteStorage(),
                                   default='user_photo/default.jpg')

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

    def __str__(self):
        """
           String for representing the model object (in Admin site etc.)
        """
        return self.get_username()
