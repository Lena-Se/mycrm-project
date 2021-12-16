import django_filters
from .constants import SORT_CHOICES
from .models import Client


class ClientFilter(django_filters.FilterSet):

    ordering = django_filters.OrderingFilter(choices=SORT_CHOICES,  empty_label=None,
                                             fields=(
                                                 ('company_name', 'компания'),
                                                 ('created', 'дата создания'),
                                                 ('updated', 'дата изменения'),
                                             ), label='сортировать по:', initial=['company_name', 'названию'])

    class Meta:
        model = Client
        fields = []





