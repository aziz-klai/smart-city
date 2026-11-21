from django.db import models

class Batiment(models.Model):
    TYPE_CHOICES = [
        ('hv', 'Hotel de ville'),
        ('bib', 'Bibliotheque'),
        ('cc', 'Centre culturel'),
        ('cs', 'Centre sportif'),
        ('sm', 'Salle municipale'),
        ('adm', 'Batiment administratif'),
        ('a', 'Autre'),
    ]
    ETAT_CHOICES = [
        ('b', 'Bon'),
        ('m', 'Moyen'),
        ('mv', 'Mauvais'),
    ]

    id_batiment = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100, null=False, blank=False)
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    adresse = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(blank=True)
    capacite = models.PositiveIntegerField(null=False, blank=False)
    horaires = models.CharField(max_length=100, blank=True)  # ex: "Lun-Ven 08:00-17:00"
    etat = models.CharField(max_length=2, choices=ETAT_CHOICES, default='b')
    date = models.DateField(null=False, blank=False)  # date de création / mise en service

    def __str__(self):
        return self.nom
