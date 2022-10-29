from django import forms
from refbooks_keeper.refbooks.models import Refbook, Version, Element


class RefbookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RefbookForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False

    class Meta:
        model = Refbook
        fields = ['id', 'code', 'name', 'description']
