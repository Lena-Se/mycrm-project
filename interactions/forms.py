from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import formset_factory, CharField, widgets, CheckboxSelectMultiple
from django.forms.models import ModelForm, ModelMultipleChoiceField

from interactions.models import Keyword, Interaction


class KeywordForm(ModelForm):
    word = CharField(required=False, min_length=1, max_length=300, label='')

    class Meta:
        model = Keyword
        fields = ['word']


KeywordFormSet = formset_factory(KeywordForm, extra=3)


class InteractionForm(ModelForm):
    keyword = ModelMultipleChoiceField(queryset=Keyword.objects.all(), widget=CheckboxSelectMultiple(), required=False,
                                       label='Ключевые слова')

    class Meta:
        model = Interaction
        fields = ['reference_channel', 'description', 'keyword']
