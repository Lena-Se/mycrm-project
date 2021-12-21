from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from .models import User


class UserDetailView(DetailView):
    model = User

    def get_context_data(self, **kwargs):
        self.object = self.request.user
        context = super(UserDetailView, self).get_context_data(**kwargs)
        return context


class UserUpdateView(UpdateView):
    """
    """
    model = User

    def get_context_data(self, **kwargs):
        self.object = self.request.user
        context = super(UserDetailView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy('crmuser-cabinett')
