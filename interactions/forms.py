"""
This module contains form-classes for interactions application

Attributes:
   KeywordFormSet: formset for adding keywords to Interaction object
"""
from django.forms import formset_factory, CharField, CheckboxSelectMultiple
from django.forms.models import ModelForm, ModelMultipleChoiceField
from interactions.models import Keyword, Interaction


class KeywordForm(ModelForm):
    """
    Class representing form for creating or updating keywords

    Attributes:
        word: char field for input of new values of keywords
    """
    word = CharField(required=False, min_length=1, max_length=300, label='')

    class Meta:
        model = Keyword
        fields = ['word']


KeywordFormSet = formset_factory(KeywordForm, extra=3)


class InteractionForm(ModelForm):
    """
    Class representing form for creating or updating interactions

    Attributes:
        keyword: multi-choice field for choosing keywords for interaction object
    """
    keyword = ModelMultipleChoiceField(queryset=Keyword.objects.all(), widget=CheckboxSelectMultiple(), required=False,
                                       label='Ключевые слова')

    class Meta:
        model = Interaction
        fields = ['reference_channel', 'description', 'keyword']
