from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from interactions.models import Interaction
from .models import User


class UserDetailView(DetailView):
    """
    Class representing view User data
    """
    model = User
    queryset = User.objects.all().prefetch_related('interaction')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        # self.object = self.request.user
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['interactions'] = Interaction.objects.filter(manager=self.object)
        return context


class UserUpdateView(UpdateView):
    """
    Class representing User data editing
    """
    model = User
    success_url = reverse_lazy('crmuser-cabinet')
    fields = ['user_photo', 'username', 'first_name', 'last_name', 'email']

    def get_object(self, queryset=None):
        return self.request.user


