from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import formset_factory
from django.forms.models import inlineformset_factory, ModelForm, ModelMultipleChoiceField

from interactions.models import Keyword, Interaction


class KeywordForm(ModelForm):
    class Meta:
        model = Keyword
        fields = ['word']


KeywordFormSet = formset_factory(KeywordForm, extra=3, can_delete=True)

# KeywordInlineFormset = inlineformset_factory(Interaction, Keyword, fields=['word'], extra=2)


class InteractionForm(ModelForm):
    keyword = ModelMultipleChoiceField(queryset=Keyword.objects.all(),
                                       widget=FilteredSelectMultiple('Ключевые слова', False), required=False)

    class Meta:
        model = Interaction
        fields = ['reference_channel', 'description', 'keyword']
