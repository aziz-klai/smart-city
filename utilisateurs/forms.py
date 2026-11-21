from datetime import date
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Utilisateur


class InformationsUtilisateurForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ('nom', 'prenom', 'email', 'telephone', 'date_naissance')
        widgets = {'date_naissance': forms.DateInput(attrs={'type': 'date'})}

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        others = Utilisateur.objects.filter(email__iexact=email)
        if self.instance.pk:
            others = others.exclude(pk=self.instance.pk)
        if others.exists():
            raise forms.ValidationError('Cet email est déjà utilisé.')
        return email

    def clean_date_naissance(self):
        value = self.cleaned_data.get('date_naissance')
        if value and value > date.today():
            raise forms.ValidationError('La date de naissance ne peut pas être dans le futur.')
        return value


class CreationUtilisateurForm(InformationsUtilisateurForm):
    role = forms.ChoiceField(choices=(('agent', 'Agent municipal'), ('admin', 'Administrateur')))
    statut = forms.ChoiceField(choices=(('actif', 'Actif'), ('inactif', 'Inactif')), required=False)
    password1 = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmation')

    def clean(self):
        data = super().clean()
        p1, p2 = data.get('password1'), data.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Les deux mots de passe sont différents.')
        elif p1 and p2:
            try:
                validate_password(p1, self.instance)
            except ValidationError as exc:
                self.add_error('password1', exc)
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = self.cleaned_data['role'] == 'admin'
        user.is_active = self.cleaned_data.get('statut', 'actif') != 'inactif'
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class ModificationUtilisateurForm(InformationsUtilisateurForm):
    role = forms.ChoiceField(choices=(('agent', 'Agent municipal'), ('admin', 'Administrateur')))
    statut = forms.ChoiceField(choices=(('actif', 'Actif'), ('inactif', 'Inactif')))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['role'].initial = 'admin' if self.instance.is_staff else 'agent'
            self.fields['statut'].initial = self.instance.statut

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = self.cleaned_data['role'] == 'admin'
        user.is_active = self.cleaned_data['statut'] == 'actif'
        if commit:
            user.save()
        return user
