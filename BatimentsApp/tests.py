import datetime

from django.test import TestCase
from django.urls import reverse

from .models import Batiment


class BatimentTests(TestCase):
    def setUp(self):
        self.batiment = Batiment.objects.create(
            nom='Hotel de ville',
            type='hv',
            adresse='1 place centrale',
            description='Accueil municipal',
            capacite=120,
            horaires='Lun-Ven 08:00-17:00',
            etat='b',
            date=datetime.date(2020, 1, 15),
        )

    def test_list_and_detail(self):
        list_response = self.client.get(reverse('Batiments:liste_batiment'))
        detail_response = self.client.get(
            reverse('Batiments:detail_batiment', args=[self.batiment.pk])
        )
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, 'Hotel de ville')
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, '1 place centrale')

    def test_create_update_and_delete(self):
        create_response = self.client.post(
            reverse('Batiments:ajouter_batiment'),
            {
                'nom': 'Bibliotheque',
                'type': 'bib',
                'adresse': '5 rue des livres',
                'description': '',
                'capacite': 80,
                'horaires': '',
                'etat': 'm',
                'date': '2024-03-10',
            },
        )
        self.assertEqual(create_response.status_code, 302)
        created = Batiment.objects.get(nom='Bibliotheque')

        update_response = self.client.post(
            reverse('Batiments:modifier_batiment', args=[created.pk]),
            {
                'nom': 'Bibliotheque centrale',
                'type': 'bib',
                'adresse': '5 rue des livres',
                'description': 'Nouvelle description',
                'capacite': 100,
                'horaires': 'Mar-Sam 09:00-18:00',
                'etat': 'b',
                'date': '2024-03-10',
            },
        )
        self.assertEqual(update_response.status_code, 302)
        created.refresh_from_db()
        self.assertEqual(created.nom, 'Bibliotheque centrale')
        self.assertEqual(created.capacite, 100)

        delete_response = self.client.post(
            reverse('Batiments:supprimer_batiment', args=[created.pk])
        )
        self.assertEqual(delete_response.status_code, 302)
        self.assertFalse(Batiment.objects.filter(pk=created.pk).exists())

    def test_search_by_name_and_id(self):
        response = self.client.get(
            reverse('Batiments:liste_batiment'),
            {'q': 'Hotel'},
        )
        self.assertContains(response, 'Hotel de ville')
