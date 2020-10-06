from django import forms

from common.models import ProtectedFile


class ProtectedFileForm(forms.ModelForm):
    class Meta:
        model = ProtectedFile
        fields = ['file']