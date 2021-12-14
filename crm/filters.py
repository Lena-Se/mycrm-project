import django_filters
from django_filters.views import FilterView
from .constants import SORT_CHOICES
from .models import Client


class ClientFilter(django_filters.FilterSet):

    ordering = django_filters.OrderingFilter(choices=SORT_CHOICES, required=True, empty_label=None)

    class Meta:
        model = Client
        fields = ['company_name']
        order_by_field = 'company_name'


