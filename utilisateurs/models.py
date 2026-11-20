from datetime import date
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UtilisateurManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Une adresse email est obligatoire.')
        email = self.normalize_email(email).strip().lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True or extra_fields.get('is_superuser') is not True:
            raise ValueError('Un superuser doit avoir is_staff et is_superuser à True.')
        return self.create_user(email, password, **extra_fields)


class Utilisateur(AbstractUser):
    """Modèle commun aux cinq apps de Smart City : email comme identifiant."""
    username = None
    nom = models.CharField(max_length=80)
    prenom = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True)
    date_naissance = models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']
    objects = UtilisateurManager()

    @property
    def statut(self):
        return 'actif' if self.is_active else 'inactif'

    def get_statut_display(self):
        return 'Actif' if self.is_active else 'Inactif'

    @property
    def age(self):
        if not self.date_naissance:
            return None
        today = date.today()
        birth = self.date_naissance
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

    def __str__(self):
        return f'{self.prenom} {self.nom} ({self.email})'
