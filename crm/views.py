import django_filters
from django.http import HttpResponseRedirect, request
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django_filters.views import FilterView

from .models import Client, Phone, Email
from .forms import PhoneInlineFormset, EmailInlineFormset


# Create your views here.


# def index(request):
#     return render(request, 'index.html')

class IndexTemplateView(generic.TemplateView):
    template_name = 'index.html'


CHOICES =[
        ["company_name", "по названию"],
        ["-company_name", "по названию (по убыванию)"],
        ["created", "по дате создания"],
        ["-created", "по дате создания (по убыванию)"],
        ["updated", "по дате изменения"],
        ["-updated", "по дате изменения (по убыванию)"],
]


class ClientFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(name='name', lookup_expr='icontains')

    ordering = django_filters.OrderingFilter(choices=CHOICES, required=True, empty_label=None)

    class Meta:
        model = Client
        fields = ['company_name']
        # order_by_field = 'company_name'
        # ordering = ['company_name', 'created', 'updated']


class ClientsListView( generic.ListView):
    model = Client
    paginate_by = 3
    template_name = 'crm/client_list.html'
    # order = 'company_name'
    # page = 1
    filter_class = ClientFilter
    # ordering = filter_class.ordering

    # def get_queryset(self):
        # new_order = self.request.GET.get('order_by', "company_name")
        # self.page = self.request.GET.get('page', self.page)
        # new_context = Client.objects.order_by(new_order)
        # return new_context

    def get_context_data(self, **kwargs):
        context = super(ClientsListView, self).get_context_data(**kwargs)
        # context['order_by'] = self.request.GET.get('order_by', "company_name")
        context['filter'] = self.filter_class
        return context

    def get_ordering(self):
        ordering = self.request.GET.get('ordering')
        return ordering


class ClientDetailView(generic.DetailView):
    model = Client


class ClientCreateView(generic.CreateView):
    model = Client
    fields = ['company_name', 'contact_person', 'description', 'address']

    def get(self,  *args, **kwargs):
        self.object = None
        formsetPhone = PhoneInlineFormset()
        formsetEmail = EmailInlineFormset()
        return self.render_to_response(self.get_context_data(phonesFormset=formsetPhone,
                                                             emailsFormset=formsetEmail))

    def post(self,  *args, **kwargs):
        formsetPhone = PhoneInlineFormset(request.POST)
        formsetEmail = EmailInlineFormset(request.POST)

        if self.form.is_valid() and formsetPhone.is_valid() and formsetEmail.is_valid():
            return self.form_valid(formsetPhone, formsetEmail)

    # def form_valid(self):
    #     super(ClientCreateView, self).form_valid()
    #     if self.form.is_valid():
    #         self.form.save()
    #         return HttpResponseRedirect(reverse_lazy('clients'))


class ClientUpdateView(generic.UpdateView):
    model = Client

    # def get(self, request, *args, **kwargs):
    #     # self.object = None
    #     # form_class = self.get_form_class()
    #     # form = self.get_form(form_class)
    #     formsetPhone = PhoneInlineFormset(instance=self.object)
    #     formsetEmail = EmailInlineFormset(instance=self.object)
    #     return self.render_to_response(
    #         self.get_context_data(phonesFormset=formsetPhone,
    #                               emailsFormset=formsetEmail))
    #
    # def post(self, request, *args, **kwargs):
    #     # self.object = None
    #     # form_class = self.get_form_class()
    #     # form = self.get_form(form_class)
    #     formsetPhone = PhoneInlineFormset(request.POST, isinstance(self.object))
    #     formsetEmail = EmailInlineFormset(request.POST,  instance=self.object)
    #
    #     if self.form.is_valid() and formsetPhone.is_valid() and formsetEmail.is_valid():
    #         return self.form_valid(formsetPhone, formsetEmail)

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
        formsetPhone = context['phonesFormset']
        formsetEmail = context['emailsFormset']
        if formsetPhone.is_valid() and formsetEmail.is_valid():
            form.save()
            # self.object = form.save()
            formsetPhone.instance = self.object
            formsetPhone.save()
            formsetEmail.instance = self.object
            formsetEmail.save()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)


    # if request.method == "POST":
    #     formsetPhone = PhoneInlineFormset(request.POST,  instance=object)
    #     if formsetPhone.is_valid():
    #         formsetPhone.save()
    #     formsetEmail = EmailInlineFormset(request.POST,  instance=object)
    #     if formsetEmail.is_valid():
    #         formsetEmail.save()
    #
    # else:
    #     formsetPhone = PhoneInlineFormset(instance=object)
    #     formsetEmail = EmailInlineFormset(instance=object)

    fields = ['company_name', 'contact_person', 'description', 'address']

    def get_success_url(self):
        return reverse_lazy('client_detail', args=[self.object.slug])
