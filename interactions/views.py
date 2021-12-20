from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from interactions.models import Interaction


class InteractionDetailView(PermissionRequiredMixin, DetailView):
    model = Interaction
    permission_required = 'interactions.view_interaction'


class InteractionCreateView(PermissionRequiredMixin, CreateView):
    model = Interaction
    # form_class = InteractionForm
    permission_required = 'interactions.add_interaction'

    def get_success_url(self):
        return reverse_lazy('project-details', args=[self.project.id])


class InteractionUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Class representing ViewForm for editing data of Interaction model object.
    Based on generic.UpdateView
    attributes:
    model - model-class representing object's data

    methods:

    """
    model = Interaction
    permission_required = 'interactions.change_interaction'

    def get_success_url(self):
        return reverse_lazy('interaction-details', args=[self.object.id])


class InteractionDeleteView(PermissionRequiredMixin, DeleteView):
    model = Interaction
    permission_required = 'interaction.delete_interaction'

    def get_success_url(self):
        return reverse_lazy('project-details', args=[self.project.id])
