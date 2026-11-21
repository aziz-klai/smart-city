from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError


# Create your models here.
class document(models.Model):
    id_doc = models.AutoField(primary_key=True)
    nom_doc = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()
    type_doc=models.CharField(max_length=50,choices=[('Autorisation','Autorisation'),('Contrat','Contrat'),('Facture', 'Facture'),('Reclamation', 'Réclamation'),('Demande administrative', 'Demande administrative'),('Decision municipale', 'Décision municipale'),
    ('Correspondance', 'Correspondance'),])
    categorie=models.CharField(max_length=50,choices=[('Etat civil', 'État civil'),('Urbanisme', 'Urbanisme et construction'),('Environnement', 'Environnement et propreté'),('Fiscalite', 'Fiscalité et taxes municipales'),('RH', 'Ressources humaines'),('Finances', 'Finances et comptabilité'),('Services administratifs', 'Services administratifs'),('Affaires juridiques', 'Affaires juridiques')])
    statut=models.CharField(max_length=20,choices=[('En_cours', 'En cours de traitement'),
        ('Valide', 'Validé'),
        ('Refuse', 'Refusé'),
        ('Archive', 'Archivé'),
        ('Annule', 'Annulé'),],default='En_cours')
    created_at= models.DateTimeField(auto_now_add=True)
    updates_at= models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.date and self.date < timezone.localdate():
            raise ValidationError({
                'date': "La date du document doit être supérieure ou égale à la date d'aujourd'hui."
            })