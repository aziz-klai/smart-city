from django import forms
from .models import Transport


class TransportForm(forms.ModelForm):
    class Meta:
        model = Transport
        fields = [
            'numeroLigne',
            'matricule_vehicule',
            'type_vehicule',
            'depart',
            'destination',
            'capacite',
            'heure_depart',
            'heure_arrivee',
            'jourdecirculation',
            'etat',
        ]
        labels = {
            'numeroLigne': 'Numéro de ligne',
            'matricule_vehicule': 'Matricule du véhicule',
            'type_vehicule': 'Type de véhicule',
            'depart': 'Départ',
            'destination': 'Destination',
            'capacite': 'Capacité (places)',
            'heure_depart': 'Heure de départ',
            'heure_arrivee': "Heure d'arrivée",
            'jourdecirculation': 'Jour de circulation',
            'etat': 'État',
        }
        widgets = {
            'numeroLigne': forms.TextInput(attrs={'class': 'input'}),
            'matricule_vehicule': forms.TextInput(attrs={'class': 'input'}),
            'type_vehicule': forms.Select(attrs={'class': 'input'}),
            'depart': forms.TextInput(attrs={'class': 'input'}),
            'destination': forms.TextInput(attrs={'class': 'input'}),
            'capacite': forms.NumberInput(attrs={'class': 'input', 'min': 1}),
            'heure_depart': forms.TimeInput(attrs={'class': 'input', 'type': 'time'}),
            'heure_arrivee': forms.TimeInput(attrs={'class': 'input', 'type': 'time'}),
            'jourdecirculation': forms.Select(attrs={'class': 'input'}),
            'etat': forms.Select(attrs={'class': 'input'}),
        }

    def clean_matricule_vehicule(self):
        matricule = self.cleaned_data['matricule_vehicule'].strip()
        if not matricule:
            raise forms.ValidationError('Le matricule du véhicule est obligatoire.')
        return matricule

    def clean_type_vehicule(self):
        type_vehicule = self.cleaned_data['type_vehicule'].strip()
        if not type_vehicule:
            raise forms.ValidationError('Le type de véhicule est obligatoire.')
        return type_vehicule

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
        heure_depart = data.get('heure_depart')
        heure_arrivee = data.get('heure_arrivee')
        if depart and destination and depart.lower() == destination.lower():
            raise forms.ValidationError("Le départ et la destination doivent être différents.")
        if heure_depart and heure_arrivee and heure_arrivee <= heure_depart:
            self.add_error(
                'heure_arrivee',
                "L'heure d'arrivée doit être postérieure à l'heure de départ.",
            )
        return data