from django.test import TestCase
from django.urls import reverse
from utilisateurs.models import Utilisateur
from .models import Evenement


class EvenementIntegrationTests(TestCase):
    def setUp(self):
        self.admin = Utilisateur.objects.create_superuser(
            email='admin@example.com',
            password='SecureTestPass123!',
            nom='Admin',
            prenom='Test',
        )
        self.agent = Utilisateur.objects.create_user(
            email='agent@example.com',
            password='SecureTestPass123!',
            nom='Agent',
            prenom='Test',
        )
        self.evenement = Evenement.objects.create(
            nom='Festival municipal',
            description='Événement de test',
            type='f',
            date_heure='2026-12-01T18:30:00Z',
            lieu='Centre-ville',
            capacite=100,
            statut='p',
        )

    def test_anonymous_users_are_sent_to_login(self):
        response = self.client.get(reverse('Evenement:liste_evenement'))
        self.assertRedirects(
            response,
            f"{reverse('utilisateurs:connexion')}?next={reverse('Evenement:liste_evenement')}",
        )

    def test_authenticated_agents_can_view_events(self):
        self.client.force_login(self.agent)
        response = self.client.get(reverse('Evenement:liste_evenement'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.evenement.nom)
        self.assertContains(response, reverse('Evenement:liste_evenement'))
        self.assertContains(response, reverse('Evenement:create_evenement'))
        self.assertContains(response, reverse('Evenement:update_evenement', args=[self.evenement.pk]))
        self.assertContains(response, reverse('Evenement:delete_evenement', args=[self.evenement.pk]))
        self.assertContains(response, reverse('utilisateurs:profil'))
        self.assertNotContains(response, reverse('utilisateurs:liste'))
        self.assertContains(response, reverse('batiments'))
        self.assertContains(response, reverse('documents'))
        self.assertContains(response, reverse('transports'))

    def test_administrator_navigation_links_both_modules(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse('Evenement:liste_evenement'))
        self.assertContains(response, reverse('Evenement:liste_evenement'))
        self.assertContains(response, reverse('utilisateurs:liste'))

    def test_agents_can_create_update_and_delete_events(self):
        self.client.force_login(self.agent)
        response = self.client.post(reverse('Evenement:create_evenement'), {
            'nom': 'Événement agent',
            'description': 'Créé par un agent municipal',
            'type': 'r',
            'date_heure': '2026-12-05T16:00',
            'lieu': 'Mairie',
            'capacite': 40,
            'statut': 'p',
        })
        self.assertRedirects(response, reverse('Evenement:liste_evenement'))
        evenement = Evenement.objects.get(nom='Événement agent')

        response = self.client.post(
            reverse('Evenement:update_evenement', args=[evenement.pk]),
            {
                'nom': 'Événement modifié',
                'description': 'Modifié par un agent municipal',
                'type': 'r',
                'date_heure': '2026-12-05T16:00',
                'lieu': 'Mairie',
                'capacite': 45,
                'statut': 'p',
            },
        )
        self.assertRedirects(response, reverse('Evenement:liste_evenement'))
        evenement.refresh_from_db()
        self.assertEqual(evenement.nom, 'Événement modifié')

        response = self.client.post(reverse('Evenement:delete_evenement', args=[evenement.pk]))
        self.assertRedirects(response, reverse('Evenement:liste_evenement'))
        self.assertFalse(Evenement.objects.filter(pk=evenement.pk).exists())

    def test_administrator_can_create_event_with_generated_id(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse('Evenement:create_evenement'), {
            'nom': 'Réunion publique',
            'description': 'Réunion de quartier',
            'type': 'r',
            'date_heure': '2026-12-05T16:00',
            'lieu': 'Mairie',
            'capacite': 40,
            'statut': 'p',
        })
        self.assertRedirects(response, reverse('Evenement:liste_evenement'))
        evenement = Evenement.objects.get(nom='Réunion publique')
        self.assertIsNotNone(evenement.pk)
