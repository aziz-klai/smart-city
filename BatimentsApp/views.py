from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .forms import BatimentForm
from .models import Batiment


class ListeBatiment(LoginRequiredMixin, ListView):
    model = Batiment
    template_name = 'Batiments/list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        recherche = self.request.GET.get('q', '').strip()
        if recherche:
            filtres = Q(nom__icontains=recherche) | Q(adresse__icontains=recherche)
            if recherche.isdigit():
                filtres |= Q(id_batiment=int(recherche))
            queryset = queryset.filter(filtres)

        type_batiment = self.request.GET.get('type', '').strip()
        if type_batiment in dict(Batiment.TYPE_CHOICES):
            queryset = queryset.filter(type=type_batiment)

        etat = self.request.GET.get('etat', '').strip()
        if etat in dict(Batiment.ETAT_CHOICES):
            queryset = queryset.filter(etat=etat)

        tri = self.request.GET.get('tri', '').strip()
        if tri in {'nom', '-nom', '-capacite', '-date', 'date'}:
            queryset = queryset.order_by(tri)
        else:
            queryset = queryset.order_by('nom')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total = Batiment.objects.count()
        bon = Batiment.objects.filter(etat='b').count()
        moyen = Batiment.objects.filter(etat='m').count()
        mauvais = Batiment.objects.filter(etat='mv').count()
        context['stats'] = {
            'total': total,
            'bon': bon,
            'moyen': moyen,
            'mauvais': mauvais,
            'repartition': self._repartition(),
        }
        return context

    @staticmethod
    def _repartition():
        total = Batiment.objects.count()
        couleurs = {
            'hv': '#2563eb',
            'bib': '#a78bfa',
            'cc': '#14b8a6',
            'cs': '#2563eb',
            'sm': '#60a5fa',
            'adm': '#0f766e',
            'a': '#94a3b8',
        }
        repartition = []
        for code, label in Batiment.TYPE_CHOICES:
            count = Batiment.objects.filter(type=code).count()
            pourcentage = round(count * 100 / total) if total else 0
            repartition.append({
                'label': label,
                'pct': pourcentage,
                'couleur': couleurs[code],
            })
        return repartition


class DetailBatiment(LoginRequiredMixin, DetailView):
    model = Batiment
    template_name = 'Batiments/detail.html'


class DeleteBatiment(LoginRequiredMixin, DeleteView):
    model = Batiment
    template_name = 'Batiments/delete.html'
    success_url = reverse_lazy('Batiments:liste_batiment')


class CreateBatiment(LoginRequiredMixin, CreateView):
    model = Batiment
    template_name = 'Batiments/form.html'
    form_class = BatimentForm
    success_url = reverse_lazy('Batiments:liste_batiment')


class UpdateBatiment(LoginRequiredMixin, UpdateView):
    model = Batiment
    template_name = 'Batiments/form.html'
    form_class = BatimentForm
    success_url = reverse_lazy('Batiments:liste_batiment')