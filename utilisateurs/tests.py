from django.test import TestCase
from django.urls import reverse
from .models import Utilisateur


class UtilisateursCRUDTests(TestCase):
    def setUp(self):
        self.admin = Utilisateur.objects.create_superuser(
            email='admin@example.com', password='SecureTestPass123!', nom='Admin', prenom='Test'
        )
        self.agent = Utilisateur.objects.create_user(
            email='agent@example.com', password='SecureTestPass123!', nom='Agent', prenom='Test'
        )

    def test_crud_admin(self):
        self.client.force_login(self.admin)
        data = {'nom': 'Dupont', 'prenom': 'Leila', 'email': 'leila@example.com',
                'telephone': '+216 12345678', 'role': 'agent', 'statut': 'actif',
                'password1': 'SecureTestPass123!', 'password2': 'SecureTestPass123!'}
        rep = self.client.post(reverse('utilisateurs:ajouter'), data)
        self.assertRedirects(rep, reverse('utilisateurs:liste'))
        created = Utilisateur.objects.get(email='leila@example.com')
        self.assertTrue(created.check_password('SecureTestPass123!'))
        self.assertContains(self.client.get(reverse('utilisateurs:liste')), 'leila@example.com')
        self.assertEqual(self.client.get(reverse('utilisateurs:detail', args=[created.pk])).status_code, 200)
        data = {'nom':'Dupont', 'prenom':'Leila', 'email':'new@example.com',
                'role':'agent', 'statut':'actif'}
        rep = self.client.post(reverse('utilisateurs:modifier', args=[created.pk]), data)
        self.assertRedirects(rep, reverse('utilisateurs:liste'))
        created.refresh_from_db()
        self.assertEqual(created.email, 'new@example.com')
        rep = self.client.post(reverse('utilisateurs:supprimer', args=[created.pk]))
        self.assertRedirects(rep, reverse('utilisateurs:liste'))
        self.assertFalse(Utilisateur.objects.filter(pk=created.pk).exists())

    def test_invalid_duplicate_email_and_password(self):
        self.client.force_login(self.admin)
        rep = self.client.post(reverse('utilisateurs:ajouter'), {
            'nom': 'Test', 'prenom': 'D', 'email': 'AGENT@example.com',
            'role':'agent', 'statut':'actif', 'password1':'test12345', 'password2':'different'
        })
        self.assertEqual(rep.status_code, 400)
        self.assertEqual(Utilisateur.objects.count(), 2)

    def test_agent_cannot_access_administration(self):
        self.client.force_login(self.agent)
        self.assertEqual(self.client.get(reverse('utilisateurs:liste')).status_code, 403)
        self.assertEqual(self.client.post(reverse('utilisateurs:supprimer', args=[self.admin.pk])).status_code, 403)

    def test_delete_requires_post(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse('utilisateurs:supprimer', args=[self.agent.pk])).status_code, 200)
        self.assertTrue(Utilisateur.objects.filter(pk=self.agent.pk).exists())

    def test_cannot_delete_self(self):
        self.client.force_login(self.admin)
        self.client.post(reverse('utilisateurs:supprimer', args=[self.admin.pk]))
        self.assertTrue(Utilisateur.objects.filter(pk=self.admin.pk).exists())

    def test_deactivate(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse('utilisateurs:desactiver', args=[self.agent.pk])).status_code, 405)
        self.client.post(reverse('utilisateurs:desactiver', args=[self.agent.pk]))
        self.agent.refresh_from_db()
        self.assertFalse(self.agent.is_active)
