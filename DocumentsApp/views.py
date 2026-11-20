from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.db.models import Q
from DocumentsApp.forms import DocumentForm
from DocumentsApp.models import document





class Liste_Document(ListView):
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

class Detail_Document(DetailView):
    model = document
    template_name = 'document/detail.html'
  

class Delete_Document(DeleteView):
    model = document
    template_name = 'document/delete.html'
    success_url = reverse_lazy('Document:listdocument')

class Create_Document(CreateView):
    model = document
    template_name = 'document/form.html'
    #fields = '__all__'
    form_class = DocumentForm
    success_url = reverse_lazy('Document:listdocument')
class Update_Document(UpdateView):
    model = document
    template_name = 'document/form.html'
    form_class = DocumentForm
    success_url = reverse_lazy('Document:listdocument')