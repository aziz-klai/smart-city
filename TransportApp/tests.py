from django.test import TestCase
from django.urls import reverse

from utilisateurs.models import Utilisateur

from .models import Transport


class TransportIntegrationTests(TestCase):
    def setUp(self):
        self.agent = Utilisateur.objects.create_user(
            email='transport-agent@example.com',
            password='SecureTestPass123!',
            nom='Agent',
            prenom='Transport',
        )

    def transport_data(self, numero_ligne='12'):
        return {
            'numeroLigne': numero_ligne,
            'matricule_vehicule': '123TU4567',
            'type_vehicule': 'Bus',
            'depart': 'Centre-ville',
            'destination': 'Gare',
            'capacite': 50,
            'heure_depart': '08:00',
            'heure_arrivee': '09:00',
            'jourdecirculation': 'lundi',
            'etat': 'actif',
        }

    def test_authenticated_agents_can_create_transports_with_all_requested_fields(self):
        self.client.force_login(self.agent)

        response = self.client.post(
            reverse('Transport:ajouter_transport'),
            self.transport_data(),
        )

        self.assertRedirects(response, reverse('Transport:liste_transports'))
        transport = Transport.objects.get(numeroLigne='12')
        self.assertEqual(transport.matricule_vehicule, '123TU4567')
        self.assertEqual(transport.type_vehicule, 'Bus')
        self.assertEqual(transport.capacite, 50)
        self.assertEqual(str(transport.heure_depart), '08:00:00')
        self.assertEqual(str(transport.heure_arrivee), '09:00:00')
        self.assertEqual(transport.jourdecirculation, 'lundi')

        response = self.client.get(reverse('Transport:liste_transports'))
        self.assertContains(response, '123TU4567')
        self.assertContains(response, 'Bus')
        self.assertContains(response, 'Lundi')
        self.assertContains(response, reverse('Transport:detail_transport', args=[transport.pk]))

    def test_authenticated_agents_can_consult_transport_details(self):
        self.client.force_login(self.agent)
        transport = Transport.objects.create(**self.transport_data())

        response = self.client.get(
            reverse('Transport:detail_transport', args=[transport.pk]),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '123TU4567')
        self.assertContains(response, 'Bus')
        self.assertContains(response, '50 places')
        self.assertContains(response, '08:00')
        self.assertContains(response, '09:00')
        self.assertContains(response, 'Lundi')

    def test_arrival_time_must_be_after_departure_time(self):
        self.client.force_login(self.agent)

        for numero_ligne, heure_arrivee in [('40', '07:59'), ('41', '08:00')]:
            data = self.transport_data(numero_ligne)
            data['heure_arrivee'] = heure_arrivee
            response = self.client.post(
                reverse('Transport:ajouter_transport'),
                data,
            )

            self.assertEqual(response.status_code, 200)
            self.assertIn('heure_arrivee', response.context['form'].errors)
            self.assertFalse(Transport.objects.filter(numeroLigne=numero_ligne).exists())

    def test_invalid_vehicle_type_is_rejected(self):
        self.client.force_login(self.agent)
        data = self.transport_data()
        data['type_vehicule'] = 'Avion'

        response = self.client.post(reverse('Transport:ajouter_transport'), data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('type_vehicule', response.context['form'].errors)
        self.assertFalse(Transport.objects.filter(numeroLigne='12').exists())
