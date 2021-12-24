#from importlib._common import _

from django.core.exceptions import ValidationError
from django.forms import DateTimeField, SelectDateWidget
from django.forms.models import inlineformset_factory, ModelForm
from .models import Client, Phone, Email, Project
from django.contrib.admin.widgets import AdminDateWidget


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = "__all__"


class PhoneForm(ModelForm):
    class Meta:
        model = Phone
        fields = ['number']


PhoneInlineFormset = inlineformset_factory(Client, Phone, fields=['number'], extra=1)
EmailInlineFormset = inlineformset_factory(Client, Email, fields=['email_address'], extra=1)


class ProjectForm(ModelForm):
    start_date = DateTimeField(widget=AdminDateWidget())
    end_date = DateTimeField(widget=AdminDateWidget(), required=False)

    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'price']

    def clean_end_date(self):
        end_data = self.cleaned_data['end_date']
        start_data = self.cleaned_data['start_date']

        # Проверка того, что дата не выходит за "нижнюю" границу (не в прошлом).
        if end_data and start_data and end_data <= start_data:
            raise ValidationError(self, message='Некорректная дата окончанчания проекта! Дата должна быть позже даты начала!')

        return end_data
