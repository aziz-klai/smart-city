from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, CreateView, UpdateView
from django.db.models import Q
from .forms import EvenementForm

from .models import Evenement
# Create your views here.

class Liste_Evenement(ListView):
    model=Evenement
    template_name='evenement/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        recherche = self.request.GET.get('q', '').strip()
        if recherche:
            filtres = Q(nom__icontains=recherche)
            if recherche.isdigit():
                filtres |= Q(id_evenement=int(recherche))
            queryset = queryset.filter(filtres)
        return queryset

class Detail_Evenement(DetailView):
    model=Evenement
    template_name='evenement/detail.html'


class Delete_Evenement(DeleteView):
    model=Evenement
    template_name='evenement/delete.html'
    success_url=reverse_lazy('Evenement:liste_evenement')  #redirection vers la liste après suppression



class Create_Evenement(CreateView):
     model=Evenement
     template_name='evenement/form.html'
     form_class = EvenementForm
     success_url=reverse_lazy('Evenement:liste_evenement')  #redirection vers la liste après création


class Update_Evenement(UpdateView):
     model=Evenement
     template_name='evenement/form.html'
     form_class = EvenementForm
     success_url=reverse_lazy('Evenement:liste_evenement')  #redirection vers la liste après mise à jour


# Create your views here.
