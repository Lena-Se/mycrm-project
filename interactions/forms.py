from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms.models import inlineformset_factory, ModelForm, ModelMultipleChoiceField

from interactions.models import Keyword, Interaction


class InteractionForm(ModelForm):
    keyword = ModelMultipleChoiceField(queryset=Keyword.objects.all(),
                                       widget=FilteredSelectMultiple('Keywords', False), required=False)

    class Meta:
        model = Interaction
        fields = ['reference_channel', 'description', 'keyword']
