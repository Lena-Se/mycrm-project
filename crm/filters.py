import django_filters
from .constants import SortChoices
from .models import Client, Project


class ClientFilter(django_filters.FilterSet):
    company_name = django_filters.CharFilter(lookup_expr='istartswith', label='Компания')
    ordering = django_filters.OrderingFilter(choices=SortChoices.choices,  empty_label=None,
                                             fields=(
                                                 ('company_name', 'компания'),
                                                 ('created', 'дата создания'),
                                                 ('updated', 'дата изменения'),
                                             ), label='сортировать по:', initial=SortChoices.COMPANY)

    class Meta:
        model = Client
        fields = ['company_name']


class ProjectFilter(django_filters.FilterSet):
    company__company_name = django_filters.ModelChoiceFilter(queryset=Client.objects.all(), label='Компания')
    name = django_filters.ModelChoiceFilter(queryset=Project.objects.all(), label='Проект')
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



