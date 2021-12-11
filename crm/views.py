import django_filters
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .models import Client, Phone, Email


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

    ordering = django_filters.OrderingFilter(choices=CHOICES, required=True, empty_label=None,)


    class Meta:
        model = Client
        fields = ['company_name']
        # order_by_field = 'company_name'


class ClientsListView(generic.ListView):
    model = Client
    paginate_by = 3
    # order = 'company_name'
    # page = 1
    filter_class = ClientFilter

    # def get_queryset(self):
    #     new_order = self.request.GET.get('order_by', self.order)
    #     self.page = self.request.GET.get('page', self.page)
    #     new_context = Client.objects.order_by(new_order)
    #     self.order = new_order
    #     return new_context

    def get_context_data(self, **kwargs):
        context = super(ClientsListView, self).get_context_data(**kwargs)
        # context['order_by'] = self.request.GET.get('order_by', "company_name")
        context['filter'] = ClientFilter(self.request.GET, queryset=Client.objects.all())
        # context['page]'] = self.request.GET.get('page', self.page)
        return context

    # def get_ordering(self):
    #     ordering = self.request.GET.get('order_by')
    #     return ordering


class ClientDetailView(generic.DetailView):
    model = Client


class ClientUpdateView(generic.UpdateView):
    model = Client


class ClientCreateView(generic.CreateView):
    model = Client


class ClientCreateView(generic.CreateView):
    model = Client
    fields = ['company_name', 'contact_person', 'description', 'address']

    def form_valid(self, form):
        super(ClientCreateView, self).form_valid(form)
        client = form.instance

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('clients'))


class ClientUpdateView(generic.UpdateView):
    model = Client
    fields = ['company_name', 'contact_person', 'description', 'address']
