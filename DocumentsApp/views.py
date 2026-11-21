from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.db.models import Q
from .forms import DocumentForm
from .models import document


class Liste_Document(LoginRequiredMixin, ListView):
    model = document
    template_name = 'document/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(id_doc__icontains=query)
                | Q(type_doc__icontains=query)
                | Q(nom_doc__icontains=query)
            )
        return queryset

class Detail_Document(LoginRequiredMixin, DetailView):
    model = document
    template_name = 'document/detail.html'

class Delete_Document(LoginRequiredMixin, DeleteView):
    model = document
    template_name = 'document/delete.html'
    success_url = reverse_lazy('Document:listdocument')

class Create_Document(LoginRequiredMixin, CreateView):
    model = document
    template_name = 'document/form.html'
    form_class = DocumentForm
    success_url = reverse_lazy('Document:listdocument')


class Update_Document(LoginRequiredMixin, UpdateView):
    model = document
    template_name = 'document/form.html'
    form_class = DocumentForm
    success_url = reverse_lazy('Document:listdocument')