from django import forms
from django.utils import timezone
from DocumentsApp.models import document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = document
        fields ="__all__"
        exclude = ['id_doc']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'input',
                'min': timezone.localdate().isoformat(),
            }),
            'nom_doc': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'class': 'input', 'rows': 4}),
            'type_doc': forms.Select(attrs={'class': 'input'}),
            'categorie': forms.Select(attrs={'class': 'input'}),
            'statut': forms.Select(attrs={'class': 'input'}),
        }

    def clean_date(self):
        date_document = self.cleaned_data['date']
        if date_document < timezone.localdate():
            raise forms.ValidationError(
                "La date du document doit être supérieure ou égale à la date d'aujourd'hui."
            )
        return date_document
        
