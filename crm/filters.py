"""
This module contains filter-classes based on django_filters for crm application
"""
import django_filters
from .constants import SortChoices
from .models import Client, Project


class ClientFilter(django_filters.FilterSet):
    """
    Class contains filterset for Client model objects filtering

    Attributes:
        company_name: char filter for filtering clients by company_name
        ordering: ordering filter for Client model objects sorting
    """
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
    """
    Class contains filterset for Project model objects filtering

    Attributes:
        company__company_name: choice filter for filtering projects by company
        name: choice filter for filtering projects by name
        ordering: ordering filter for Project model objects sorting
    """
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



