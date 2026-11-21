from django.db import models
from django.core.validators import MinValueValidator

class Transport(models.Model):
    TYPE_VEHICULE_CHOICES = [
        ('Bus', 'Bus'),
        ('Minibus', 'Minibus'),
        ('Tramway', 'Tramway'),
        ('Métro', 'Métro'),
        ('Trolleybus', 'Trolleybus'),
        ('Train', 'Train'),
        ('Taxi collectif', 'Taxi collectif'),
        ('Autre', 'Autre'),
    ]

    JOUR_CIRCULATION_CHOICES = [
        ('lundi', 'Lundi'),
        ('mardi', 'Mardi'),
        ('mercredi', 'Mercredi'),
        ('jeudi', 'Jeudi'),
        ('vendredi', 'Vendredi'),
        ('samedi', 'Samedi'),
        ('dimanche', 'Dimanche'),
        ('tous_les_jours', 'Tous les jours'),
    ]

    ETAT_CHOICES = [
        ('actif', 'Actif'),
        ('maintenance', 'En maintenance'),
        ('hors_service', 'Hors service'),
    ]
    numeroLigne = models.CharField(max_length=20)
    depart = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    matricule_vehicule = models.CharField(max_length=20, null=True)
    type_vehicule = models.CharField(
        max_length=50,
        choices=TYPE_VEHICULE_CHOICES,
        null=True,
    )
    capacite = models.PositiveIntegerField(
        null=True,
        validators=[MinValueValidator(1)],
    )
    heure_depart = models.TimeField(null=True)
    heure_arrivee = models.TimeField(null=True)
    jourdecirculation = models.CharField(
        max_length=20,
        choices=JOUR_CIRCULATION_CHOICES,
        null=True,
    )
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='actif')
    dateCreation = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Ligne {self.numeroLigne} : {self.depart} → {self.destination}"