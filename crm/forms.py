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
