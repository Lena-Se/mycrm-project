from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from crm.models import Project
from interactions.models import Interaction


class InteractionDetailView(PermissionRequiredMixin, DetailView):
    model = Interaction
    permission_required = 'interactions.view_interaction'


class InteractionCreateView(PermissionRequiredMixin, CreateView):
    model = Interaction
    # form_class = InteractionForm
    permission_required = 'interactions.add_interaction'
    fields = ['reference_channel', 'description']
    project = None

    def get_context_data(self, **kwargs):
        context = super(InteractionCreateView, self).get_context_data(**kwargs)
        self.project = get_object_or_404(Project, id=self.kwargs['project_id'])
        print(self.project)
        context['project'] = self.project
        context['client'] = self.project.company
        return context

    def post(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, id=self.kwargs['project_id'])
        return super().post(request, *args, kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.project = self.project
        self.object.manager = self.request.user
        self.object.save()
        return super(InteractionCreateView, self).form_valid(form)

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
    fields = ['reference_channel', 'description']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.manager = self.request.user
        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('interaction-details', args=[self.object.id])


class InteractionDeleteView(PermissionRequiredMixin, DeleteView):
    model = Interaction
    permission_required = 'interaction.delete_interaction'

    def get_success_url(self):
        return reverse_lazy('project-details', args=[self.project.id])
