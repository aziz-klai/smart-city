from django.db import models

class Transport(models.Model):
    ETAT_CHOICES = [
        ('actif', 'Actif'),
        ('maintenance', 'En maintenance'),
        ('hors_service', 'Hors service'),
    ]
    numeroLigne = models.CharField(max_length=20)
    depart = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='actif')
    dateCreation = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Ligne {self.numeroLigne} : {self.depart} → {self.destination}"