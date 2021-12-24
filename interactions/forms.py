from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms.models import inlineformset_factory, ModelForm, ModelMultipleChoiceField

from interactions.models import Keyword, Interaction

# KeywordInlineFormset = inlineformset_factory(Interaction, Keyword, fields=['word'], extra=2)


class InteractionForm(ModelForm):
    keyword = ModelMultipleChoiceField(queryset=Keyword.objects.all(),
                                       widget=FilteredSelectMultiple('Keywords', False), required=False)

    class Meta:
        model = Interaction
        fields = ['reference_channel', 'description', 'keyword']
