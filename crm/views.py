from django.shortcuts import render
from django.views import generic
from .models import Client, Phone, Email


# Create your views here.


# def index(request):
#     return render(request, 'index.html')

class IndexTemplateView(generic.TemplateView):
    template_name = 'index.html'


class ClientsListView(generic.ListView):
    model = Client
    paginate_by = 3

    def get_ordering(self):
        ordering = self.request.GET.get('order_by')
        print(ordering)
        return ordering


class ClientDetailView(generic.DetailView):
    model = Client
