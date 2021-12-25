import django_filters
from django.contrib.auth import get_user_model

from crm.models import Project, Client
from .models import Interaction, Keyword


class InteractionFilter(django_filters.FilterSet):
    projects = Project.objects.all()
    clients = Client.objects.all()
    managers = get_user_model().objects.all()
    keywords = Keyword.objects.all()
    project__name = django_filters.ModelChoiceFilter(queryset=projects, label='Проект')
    project__company__company_name = django_filters.ModelChoiceFilter(queryset=clients, label='Компания')
    manager__username = django_filters.ModelChoiceFilter(queryset=managers, label='Менеджер')
    keyword__word = django_filters.ModelMultipleChoiceFilter(queryset=keywords, label='Ключевые слова')

    ordering = django_filters.OrderingFilter(empty_label=None,
                                             fields=(
                                                 ('project', 'проект'),
                                                 ('reference_channel', 'канал обращения'),
                                                 ('rating', 'рейтинг'),
                                             ), label='сортировать по:', initial=['project', 'проект'])

    class Meta:
        model = Interaction
        fields = []


