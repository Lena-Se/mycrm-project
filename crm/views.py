"""
This module contains class-based views for crm application representing
"""
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from interactions.models import Interaction
from .filters import ClientFilter, ProjectFilter
from .models import Client, Project
from .forms import PhoneInlineFormset, EmailInlineFormset, ProjectForm


class IndexTemplateView(LoginRequiredMixin, generic.TemplateView):
    """
    Class representing view page from template
    Attributes:
        template_name (str): name of template file for view
    """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        """
        overrides standard get_context_data method, extends context with additional data about clients and projects
        """
        context = super().get_context_data(**kwargs)
        context['client_count'] = Client.objects.all().count()
        context['project_count'] = Project.objects.all().count()
        context['interaction_count'] = Interaction.objects.all().count()
        return context


class FilteredListView(generic.ListView):
    """
    Base class for making filtered listviews.
    Attributes:
        filterset_class: class with set of filters
    """
    filterset_class = None

    def get_queryset(self):
        # Get the queryset however you usually would.  For example:
        queryset = super().get_queryset()
        # Then use the query parameters and the queryset to
        # instantiate a filterset and save it as an attribute
        # on the view instance for later.
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        # Return the filtered queryset
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        context['filterset'] = self.filterset
        return context


class ClientsListView(LoginRequiredMixin, FilteredListView):
    """
    Class representing View displaying list of all Client model objects.
    Attributes:
        model: object model for listview
        paginate_by (int): count of objects on page
        paginate_orphans (int): min count of objects on last page
        filteerset_class: class containing set of filters for objects list
    """
    model = Client
    paginate_by = 3
    paginate_orphans = 1
    filterset_class = ClientFilter


class ClientDetailView(LoginRequiredMixin, generic.DetailView):
    """
    Class representing View displaying data of single Client model object.
    Attributes:
        model: object model for view details
    """
    model = Client


class ClientCreateView(PermissionRequiredMixin, generic.CreateView):
    """
    Class representing ViewForm for creating new Client.
    Attributes:
        model (class): model-class representing object's data
        fields (list): list of fields for displaying on form
        permission_required (str): name of permission required to see the result page
    """
    model = Client
    fields = ['company_name', 'contact_person', 'description', 'address']
    permission_required = 'crm.add_client'

    def get_context_data(self, **kwargs):
        """
        Overriding the standard get_context_data method to expand the context with inlineFormSets of related data.
        Returns extended context.
        """
        context = super(ClientCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['phonesFormset'] = PhoneInlineFormset(self.request.POST)
            context['phonesFormset'].full_clean()
            context['emailsFormset'] = EmailInlineFormset(self.request.POST)
            context['phonesFormset'].full_clean()
        else:
            context['phonesFormset'] = PhoneInlineFormset()
            context['emailsFormset'] = EmailInlineFormset()
        return context

    def form_valid(self, form):
        """
        Ovverrides form_valid method to save data from inlineFormSets of related data.
        """
        context = self.get_context_data(form=form)
        formset_phone = context['phonesFormset']
        formset_email = context['emailsFormset']
        if formset_phone.is_valid() and formset_email.is_valid():
            self.object = form.save()
            formset_phone.instance = self.object
            formset_phone.save()
            formset_email.instance = self.object
            formset_email.save()
            self.object.save()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        """
        Returns url for redirect on successful create object
        """
        return reverse_lazy('client-details', args=[self.object.slug])


class ClientUpdateView(generic.UpdateView):
    """
    Class representing ViewForm for editing data for object of Client model.
    Attributes:
        model (str): model-class representing object's data
        fields (list): list of fields for displaying on form
        permission_required (str): name of permission required to see the result page
    """
    model = Client
    fields = ['company_name', 'contact_person', 'description', 'address']
    permission_required = 'crm.change_client'

    def get_context_data(self, **kwargs):
        """
        Overriding the standard get_context_data method to expand the context with inlineFormSets of related data.
        Returns extended context.
        """
        context = super(ClientUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['phonesFormset'] = PhoneInlineFormset(self.request.POST, instance=self.object)
            context['phonesFormset'].full_clean()
            context['emailsFormset'] = EmailInlineFormset(self.request.POST, instance=self.object)
            context['phonesFormset'].full_clean()
        else:
            context['phonesFormset'] = PhoneInlineFormset(instance=self.object)
            context['emailsFormset'] = EmailInlineFormset(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset_phone = context['phonesFormset']
        formset_email = context['emailsFormset']
        if formset_phone.is_valid() and formset_email.is_valid():
            self.object = form.save(commit=False)
            formset_phone.instance = self.object
            formset_phone.save()
            formset_email.instance = self.object
            formset_email.save()
            self.object.save()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        """
        Returns url for redirect on successful update object
        """
        return reverse_lazy('client-details', args=[self.object.slug])


class ClientDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """
    Class for deleting Client objects
    """
    model = Client  # model-class of deleting object
    success_url = reverse_lazy('clients')  # url for redirection on success
    permission_required = 'crm.delete_client'  # (str) permission that required to see this page


class ProjectsListView(LoginRequiredMixin, FilteredListView):
    """
    Class representing projects list display
    """
    model = Project  # object model class
    paginate_by = 3  # (int) count of objects on page
    paginate_orphans = 1  # (int) min count of objects on page
    filterset_class = ProjectFilter  # class with set of filters for Project model


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    """
    Class representing single Project model object view
    Attributes:
        model: object model class
    """
    model = Project


class ProjectCreateView(PermissionRequiredMixin, generic.CreateView):
    """
    Class representing ViewForm for creating new Client.
    """
    model = Project  # model object class
    form_class = ProjectForm  # model form for creating object
    client = None  # related object
    permission_required = 'crm.add_project'  # permission to see the page

    def get_context_data(self, **kwargs):
        """
        Returns context extended with Client object derived from slug in request.
        """
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        self.client = get_object_or_404(Client, slug=self.kwargs['client_slug'])
        context['client'] = self.client
        return context

    def post(self, request, *args, **kwargs):
        """
        Extends post method with Client object data for Project company field
        """
        self.client = get_object_or_404(Client, slug=self.kwargs['client_slug'])
        return super().post(request, *args, kwargs)

    def form_valid(self, form):
        """
        Overrides form_valid method to add Client datd for new Project object
        """
        self.object = form.save(commit=False)
        self.object.company = self.client
        self.object.save()
        return super(ProjectCreateView, self).form_valid(form)

    def get_success_url(self):
        """
        Returns url for redirect on successful create object
        """
        return reverse_lazy('project-details', args=[self.object.pk])


class ProjectUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """
    Class representing ViewForm for editing data for object of Project model.
    Based on generic.UpdateView
    attributes:
    model - model-class representing object's data
    """
    model = Project  # model object class
    form_class = ProjectForm  # model form for updating object
    permission_required = 'crm.change_project'  # permission to see the page

    def get_success_url(self):
        """
          Returns url for redirect on successful update object
        """
        return reverse_lazy('project-details', args=[self.object.id])


class ProjectDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """
    Class for deleting Client objects
    """
    model = Project  # model object class
    success_url = reverse_lazy('projects')  # # url for redirection on success
    permission_required = 'crm.delete_project'  # permission to see the page
