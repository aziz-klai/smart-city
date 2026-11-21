from django import forms
from .models import Transport


class TransportForm(forms.ModelForm):
    class Meta:
        model = Transport
        fields = ['numeroLigne', 'depart', 'destination', 'etat']
        labels = {
            'numeroLigne': 'Numéro de ligne',
            'depart': 'Départ',
            'destination': 'Destination',
            'etat': 'État',
        }

    def clean_numeroLigne(self):
        n = self.cleaned_data['numeroLigne'].strip()
        if not n:
            raise forms.ValidationError("Le numéro de ligne est obligatoire.")
        return n

    def clean_depart(self):
        d = self.cleaned_data['depart'].strip()
        if len(d) < 2:
            raise forms.ValidationError("Le départ doit contenir au moins 2 caractères.")
        return d

    def clean_destination(self):
        d = self.cleaned_data['destination'].strip()
        if len(d) < 2:
            raise forms.ValidationError("La destination doit contenir au moins 2 caractères.")
        return d

    def clean(self):
        data = super().clean()
        depart = data.get('depart')
        destination = data.get('destination')
        if depart and destination and depart.lower() == destination.lower():
            raise forms.ValidationError("Le départ et la destination doivent être différents.")
        return data