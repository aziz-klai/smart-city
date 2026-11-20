from django.db import models


class Evenement(models.Model):
    id_evenement = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=20, null=False, blank=False)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=[('cul','Culturel'), ('s','Sportif'), ('conf','Conference'), ('r','Reunion'), ('f','Festival'), ('a','Autre')])
    date_heure = models.DateTimeField(null=False, blank=False)
    lieu = models.CharField(max_length=20, null=False, blank=False)
    capacite = models.PositiveIntegerField(null=False, blank=False)
    statut = models.CharField(max_length=20, choices=[('p','Prevu'), ('EC','En_cours'), ('t','Termine'), ('a','Annule')])



# Create your models here.
