import django_filters
from .models import Interaction



class InteractionFilter(django_filters.FilterSet):
    project__name = django_filters.CharFilter(lookup_expr='iexact', label='Проект')
    project__company__company_name = django_filters.CharFilter(lookup_expr='iexact', label='Компания')
   # manager__get_user_name = django_filters.CharFilter(lookup_expr='iexact', label='Менеджер')
    #  keyword__word = django_filters.MultipleChoiceFilter()

    ordering = django_filters.OrderingFilter(empty_label=None,
                                             fields=(
                                                 ('project', 'проект'),
                                                 ('reference_channel', 'канал обращения'),
                                             ), label='сортировать по:', initial=['company', 'компания'])

    class Meta:
        model = Interaction
        fields = []


