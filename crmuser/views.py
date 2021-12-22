from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from .models import User


class UserDetailView(DetailView):
    model = User

    def get_object(self, queryset=None):
        return self.request.user

    # def get_context_data(self, **kwargs):
    #     self.object = self.request.user
    #     context = super(UserDetailView, self).get_context_data(**kwargs)
    #     return context


class UserUpdateView(UpdateView):
    """
    """
    model = User
    success_url = 'crmuser-cabinet'
    fields = ['user_photo', 'username', 'first_name', 'last_name', 'email']

    def get_object(self, queryset=None):
        return self.request.user

    # def get_context_data(self, **kwargs):
    #     self.object = self.request.user
    #     context = super(UserDetailView, self).get_context_data(**kwargs)
    #     return context

    # def get_success_url(self):
    #     return reverse_lazy('crmuser-cabinet')
