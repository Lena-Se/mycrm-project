# from django.http import HttpResponseRedirect, request
# from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django_filters.views import FilterView

from .filters import ClientFilter, ProjectFilter
from .models import Client, Project
from .forms import PhoneInlineFormset, EmailInlineFormset


# Create your views here.
class IndexTemplateView(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client_count'] = Client.objects.all().count()
        context['project_count'] = Project.objects.all().count()
        return context


class FilteredListView(generic.ListView):
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


class ClientsListView(FilteredListView):  # (FilterView):  # (FilteredListView):
    model = Client
    paginate_by = 3
    paginate_orphans = 1
    template_name = 'crm/client_list.html'
    filterset_class = ClientFilter


class ClientDetailView(generic.DetailView):
    model = Client


class ClientCreateView(generic.CreateView):
    model = Client
    fields = ['company_name', 'contact_person', 'description', 'address', 'slug']
    success_url = reverse_lazy('clients')

    def get_context_data(self, **kwargs):
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
        context = self.get_context_data(form=form)
        formset_phone = context['phonesFormset']
        formset_email = context['emailsFormset']
        if formset_phone.is_valid() and formset_email.is_valid():
            form.save()
            formset_phone.instance = self.object
            formset_phone.save()
            formset_email.instance = self.object
            formset_email.save()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    # def get_success_url(self):
    #     return reverse_lazy('clients')


class ClientUpdateView(generic.UpdateView):
    """
    Class representing ViewForm for editing data for object of Client model.
    Based on generic.UpdateView
    attributes:
    model - model-class representing object's data
    fields - list of fields for displaying on form

    methods:
    get_context_data(self, **kwargs) - overriding the standard get_context_data method for
    to expand the context with inlineFormSets of related data.
    Returns extended context.
    """
    model = Client

    def get_context_data(self, **kwargs):
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
            form.save()
            # self.object = form.save()
            formset_phone.instance = self.object
            formset_phone.save()
            formset_email.instance = self.object
            formset_email.save()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    fields = ['company_name', 'contact_person', 'description', 'address']

    def get_success_url(self):
        return reverse_lazy('client-details', args=[self.object.slug])


class ProjectsListView(FilteredListView):
    model = Project
    paginate_by = 5
    paginate_orphans = 1
    template_name = 'crm/project_list.html'
    filterset_class = ProjectFilter


class ProjectDetailView(generic.DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        client = get_object_or_404(Client, slug=self.kwargs['slug'])
        context['client'] = client
        return context



class ProjectCreateView(generic.CreateView):
    model = Project
    fields = ['name', 'description', 'start_date', 'end_date', 'price']
    client = Nones

    def get_context_data(self, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        self.client = get_object_or_404(Client, slug=self.kwargs['client_slug'])
        context['client'] = self.client
        return context

    def get_success_url(self):
        return reverse_lazy('client-details', args=[self.client.slug])


class ProjectUpdateView(generic.UpdateView):
    """
    Class representing ViewForm for editing data for object of Project model.
    Based on generic.UpdateView
    attributes:
    model - model-class representing object's data
    fields - list of fields for displaying on form

    methods:
    get_context_data(self, **kwargs) - overriding the standard get_context_data method for
    to expand the context with inlineFormSets of related data.
    Returns extended context.
    """
    model = Client
    fields = ['name', 'description', 'start_date', 'end_date', 'price']

    def get_success_url(self):
        return reverse_lazy('client-details', args=[self.object.company.slug])
