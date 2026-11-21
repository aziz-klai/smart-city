from django import forms
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
            }),
            'nom_doc': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'class': 'input', 'rows': 4}),
            'type_doc': forms.Select(attrs={'class': 'input'}),
            'categorie': forms.Select(attrs={'class': 'input'}),
            'statut': forms.Select(attrs={'class': 'input'}),
        }
        
