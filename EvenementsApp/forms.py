from .models import Evenement
from django import forms


class EvenementForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = "__all__"
        exclude = ['id_evenement',]  # Exclure les champs de date de création et de mise à jour 
        widgets = {
            'date_heure': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'input',
                },
                format='%Y-%m-%dT%H:%M',
            ),
        }