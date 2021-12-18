import django_filters
from .constants import SORT_CHOICES
from .models import Client, Project


class ClientFilter(django_filters.FilterSet):
    company_name = django_filters.CharFilter(lookup_expr='istartswith', label='Компания')
    ordering = django_filters.OrderingFilter(choices=SORT_CHOICES,  empty_label=None,
                                             fields=(
                                                 ('company_name', 'компания'),
                                                 ('created', 'дата создания'),
                                                 ('updated', 'дата изменения'),
                                             ), label='сортировать по:', initial=['company_name', 'названию'])

    class Meta:
        model = Client
        fields = ['company_name']


class ProjectFilter(django_filters.FilterSet):
    company__company_name = django_filters.CharFilter(lookup_expr='iexact', label='Компания')
    name = django_filters.CharFilter(lookup_expr='istartswith', label='Проект')
    ordering = django_filters.OrderingFilter(empty_label=None,
                                             fields=(
                                                 ('company', 'компания'),
                                                 ('name', 'название'),
                                                 ('start_date', 'срок начала'),
                                                 ('end_date', 'срок окончания'),
                                                 ('price', 'стоимость'),
                                             ), label='сортировать по:', initial=['company', 'компания'])

    class Meta:
        model = Project
        fields = ['name']



