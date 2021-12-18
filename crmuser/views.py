from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from .models import User


class UserDetailView(DetailView):
    model = User


class UserUpdateView(UpdateView):
    """
    """
    model = User

    def get_success_url(self):
        return reverse_lazy('crmuser-cabinet', args=[self.name])
