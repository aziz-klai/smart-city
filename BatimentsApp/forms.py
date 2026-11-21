from django import forms

from .models import Batiment


class BatimentForm(forms.ModelForm):
    class Meta:
        model = Batiment
        fields = [
            'nom',
            'type',
            'adresse',
            'description',
            'capacite',
            'horaires',
            'etat',
            'date',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
