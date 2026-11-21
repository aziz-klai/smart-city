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

    def test_utilisateurs_root_displays_email_login(self):
        response = self.client.get(reverse('utilisateurs:connexion'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')

    def test_authenticated_visits_to_login_url_still_show_login_form(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse('utilisateurs:connexion'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Connexion')

    def test_login_redirects_to_events(self):
        response = self.client.post(reverse('utilisateurs:connexion'), {
            'username': self.admin.email,
            'password': 'SecureTestPass123!',
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_logout_returns_to_login(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse('utilisateurs:deconnexion'))
        self.assertRedirects(response, reverse('utilisateurs:connexion'))
        self.assertRedirects(
            self.client.get(reverse('Evenement:liste_evenement')),
            f"{reverse('utilisateurs:connexion')}?next={reverse('Evenement:liste_evenement')}",
        )

    def test_root_redirects_to_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('utilisateurs:connexion'), response['Location'])

    def test_dashboard_describes_project_and_links_all_four_modules(self):
        self.client.force_login(self.agent)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'application web interne')
        for module_url in (
            reverse('Evenement:liste_evenement'),
            reverse('batiments'),
            reverse('documents'),
            reverse('transports'),
        ):
            self.assertContains(response, module_url)

    def test_placeholder_modules_require_login(self):
        for module_name in ('batiments', 'documents', 'transports'):
            response = self.client.get(reverse(module_name))
            self.assertEqual(response.status_code, 302)
            self.assertIn(reverse('utilisateurs:connexion'), response['Location'])
        self.client.force_login(self.agent)
        response = self.client.get(reverse('batiments'))
        self.assertContains(response, 'Module bientôt disponible')

    def test_registration_creates_a_non_admin_account(self):
        registration_page = self.client.get(reverse('utilisateurs:inscription'))
        self.assertContains(registration_page, 'Créer un compte')
        response = self.client.post(reverse('utilisateurs:inscription'), {
            'nom': 'Nouveau',
            'prenom': 'Agent',
            'email': 'new-agent@example.com',
            'telephone': '+216 12345678',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })
        self.assertRedirects(response, reverse('utilisateurs:connexion'))
        user = Utilisateur.objects.get(email='new-agent@example.com')
        self.assertTrue(user.check_password('ComplexPass123!'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_agent_can_update_own_profile(self):
        self.client.force_login(self.agent)
        response = self.client.post(reverse('utilisateurs:profil'), {
            'nom': 'Agent modifié',
            'prenom': 'Test',
            'email': 'agent-updated@example.com',
            'telephone': '+216 98765432',
            'date_naissance': '',
        })
        self.assertRedirects(response, reverse('utilisateurs:profil'))
        self.agent.refresh_from_db()
        self.assertEqual(self.agent.email, 'agent-updated@example.com')
        self.assertEqual(self.agent.telephone, '+216 98765432')
        self.assertFalse(self.agent.is_staff)

    def test_registration_rejects_duplicate_email(self):
        response = self.client.post(reverse('utilisateurs:inscription'), {
            'nom': 'Agent',
            'prenom': 'Deux',
            'email': self.agent.email.upper(),
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Utilisateur.objects.count(), 2)

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
