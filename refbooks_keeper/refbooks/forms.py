from django import forms
from refbooks_keeper.refbooks.models import Refbook, Version, Element


class RefbookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RefbookForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False

    class Meta:
        model = Refbook
        fields = ['code', 'name', 'description']


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['refbook', 'name', 'start_date']


class ElementVersionChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return 'refbook: %s - version: %s' % (obj.refbook.code, obj.name)


class ElementAdminForm(forms.ModelForm):
    version = ElementVersionChoiceField(queryset=Version.objects.all())

    class Meta:
        model = Element
        fields = '__all__'
