from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TransportForm
from .models import Transport


def liste_transports(request):
    q = request.GET.get('q', '').strip()
    transports = Transport.objects.all().order_by('numeroLigne')
    if q:
        transports = transports.filter(
            Q(numeroLigne__icontains=q) |
            Q(depart__icontains=q) |
            Q(destination__icontains=q)
        )
    return render(request, 'transport/liste.html', {'transports': transports, 'q': q})


def ajouter_transport(request):
    form = TransportForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Transport ajouté avec succès.")
        return redirect('Transport:liste_transports')
    return render(request, 'transport/form.html', {'form': form, 'titre': 'Ajouter un transport', 'modifier': False})


def modifier_transport(request, id):
    transport = get_object_or_404(Transport, id=id)
    form = TransportForm(request.POST or None, instance=transport)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Transport modifié avec succès.")
        return redirect('Transport:liste_transports')
    return render(request, 'transport/form.html', {'form': form, 'titre': 'Modifier le transport', 'modifier': True})


def supprimer_transport(request, id):
    transport = get_object_or_404(Transport, id=id)
    if request.method == 'POST':
        transport.delete()
        messages.success(request, "Transport supprimé.")
        return redirect('Transport:liste_transports')
    return render(request, 'transport/confirmer_suppression.html', {'transport': transport})