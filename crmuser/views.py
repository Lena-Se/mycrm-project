"""
This module contains class-based views for crmuser application representing
"""
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from .models import User


class UserDetailView(DetailView):
    """
    Class representing view of User data
    """
    model = User  # model object class
    queryset = User.objects.all().prefetch_related('interaction')  # set of model objects

    def get_object(self, queryset=None):
        """
        Returns View base object
        """
        return self.request.user


class UserUpdateView(UpdateView):
    """
    Class representing User data editing
    """
    model = User  # model object class
    success_url = reverse_lazy('crmuser-cabinet')  # url for redirect on successful update
    fields = ['user_photo', 'username', 'first_name', 'last_name', 'email']  # list of field to display on edit-form

    def get_object(self, queryset=None):
        """
        Returns View base object
        """
        return self.request.user


