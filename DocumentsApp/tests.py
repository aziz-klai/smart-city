import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from utilisateurs.models import Utilisateur
from .models import document


class DocumentIntegrationTests(TestCase):
    def setUp(self):
        self.agent = Utilisateur.objects.create_user(
            email='agent@example.com',
            password='SecureTestPass123!',
            nom='Agent',
            prenom='Test',
        )

    def document_data(self, nom_doc='Autorisation de travaux'):
        return {
            'nom_doc': nom_doc,
            'date': timezone.localdate().isoformat(),
            'description': 'Document municipal de test',
            'type_doc': 'Autorisation',
            'categorie': 'Urbanisme',
            'statut': 'En_cours',
        }

    def test_anonymous_users_are_sent_to_login(self):
        response = self.client.get(reverse('Document:listdocument'))
        self.assertRedirects(
            response,
            f"{reverse('utilisateurs:connexion')}?next={reverse('Document:listdocument')}",
        )

    def test_authenticated_agents_can_create_update_view_and_delete_documents(self):
        self.client.force_login(self.agent)

        response = self.client.post(
            reverse('Document:createdocument'),
            self.document_data(),
        )
        self.assertRedirects(response, reverse('Document:listdocument'))
        item = document.objects.get(nom_doc='Autorisation de travaux')
        self.assertGreater(item.pk, 0)

        response = self.client.get(reverse('Document:listdocument'))
        self.assertContains(response, item.nom_doc)
        self.assertContains(response, reverse('Evenement:liste_evenement'))
        self.assertContains(response, reverse('utilisateurs:profil'))

        response = self.client.get(reverse('Document:detaildocument', args=[item.pk]))
        self.assertContains(response, item.description)

        response = self.client.post(
            reverse('Document:updatedocument', args=[item.pk]),
            self.document_data('Autorisation modifiée'),
        )
        self.assertRedirects(response, reverse('Document:listdocument'))
        item.refresh_from_db()
        self.assertEqual(item.nom_doc, 'Autorisation modifiée')

        response = self.client.post(reverse('Document:deletedocument', args=[item.pk]))
        self.assertRedirects(response, reverse('Document:listdocument'))
        self.assertFalse(document.objects.filter(pk=item.pk).exists())

    def test_document_search_filters_by_name(self):
        self.client.force_login(self.agent)
        document.objects.create(**self.document_data('Contrat de voirie'))
        document.objects.create(**self.document_data('Facture municipale'))

        response = self.client.get(reverse('Document:listdocument'), {'q': 'voirie'})

        self.assertContains(response, 'Contrat de voirie')
        self.assertNotContains(response, 'Facture municipale')

    def test_document_date_cannot_be_in_the_past(self):
        self.client.force_login(self.agent)
        data = self.document_data('Document trop ancien')
        data['date'] = (timezone.localdate() - datetime.timedelta(days=1)).isoformat()

        response = self.client.post(reverse('Document:createdocument'), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'La date du document doit',
        )
        self.assertFalse(document.objects.filter(nom_doc='Document trop ancien').exists())
