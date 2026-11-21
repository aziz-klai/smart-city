from functools import wraps
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CreationUtilisateurForm, ModificationUtilisateurForm, InformationsUtilisateurForm
from .models import Utilisateur


def administrateur_requis(view):
    @login_required
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied('Accès réservé aux administrateurs.')
        return view(request, *args, **kwargs)
    return wrapper


@login_required
def accueil(request):
    return redirect('utilisateurs:liste' if request.user.is_staff else 'profil')


def contexte_liste(request, formulaire=None):
    utilisateurs = Utilisateur.objects.all().order_by('nom', 'prenom')
    # Options de recherche du template déjà fournies par le groupe ; Sprint 2.
    q = request.GET.get('q', '').strip()
    if q:
        utilisateurs = utilisateurs.filter(Q(nom__icontains=q) | Q(prenom__icontains=q) | Q(email__icontains=q))
    statut = request.GET.get('statut')
    if statut == 'actif':
        utilisateurs = utilisateurs.filter(is_active=True)
    elif statut == 'inactif':
        utilisateurs = utilisateurs.filter(is_active=False)
    age = request.GET.get('age')
    if age:
        ages = {
            '18-25': lambda a: 18 <= a <= 25,
            '26-35': lambda a: 26 <= a <= 35,
            '36-50': lambda a: 36 <= a <= 50,
            '50+': lambda a: a > 50,
        }
        if age in ages:
            ids = [u.pk for u in utilisateurs if u.age is not None and ages[age](u.age)]
            utilisateurs = utilisateurs.filter(pk__in=ids)
    tri = request.GET.get('tri')
    if tri in ('nom', '-nom', '-date_joined', 'date_naissance'):
        utilisateurs = utilisateurs.order_by(tri)
    tous = Utilisateur.objects.all()
    ages = [u.age for u in tous if u.age is not None]
    segments = [
        ('18-25', lambda a: 18 <= a <= 25, '#0d9488'),
        ('26-35', lambda a: 26 <= a <= 35, '#0ea5e9'),
        ('36-50', lambda a: 36 <= a <= 50, '#f59e0b'),
        ('50+', lambda a: a > 50, '#64748b'),
    ]
    repartition = [
        {'label': label, 'pct': round(sum(check(a) for a in ages) * 100 / len(ages)) if ages else 0, 'couleur': couleur}
        for label, check, couleur in segments
    ]
    stats = {
        'total': tous.count(),
        'actifs': tous.filter(is_active=True).count(),
        'inactifs': tous.filter(is_active=False).count(),
        'age_moyen': round(sum(ages) / len(ages)) if ages else '—',
        'repartition': repartition,
    }
    return {
        'page_obj': Paginator(utilisateurs, 10).get_page(request.GET.get('page')),
        'stats': stats,
        'form': formulaire or CreationUtilisateurForm(),
    }


@administrateur_requis
def liste(request):
    return render(request, 'utilisateurs/liste.html', contexte_liste(request))


@administrateur_requis
def ajouter(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    form = CreationUtilisateurForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Utilisateur créé avec succès.')
        return redirect('utilisateurs:liste')
    return render(request, 'utilisateurs/liste.html', contexte_liste(request, form), status=400)


@administrateur_requis
def detail(request, pk):
    user_obj = get_object_or_404(Utilisateur, pk=pk)
    return render(request, 'utilisateurs/detail.html', {'user_obj': user_obj})


@administrateur_requis
def modifier(request, pk):
    user_obj = get_object_or_404(Utilisateur, pk=pk)
    form = ModificationUtilisateurForm(request.POST or None, instance=user_obj)
    if request.method == 'POST' and form.is_valid():
        new_is_staff = form.cleaned_data['role'] == 'admin'
        new_is_active = form.cleaned_data['statut'] == 'actif'
        # Empêcher de désactiver son propre compte ou de retirer ses droits admin.
        if user_obj.pk == request.user.pk and (not new_is_staff or not new_is_active):
            form.add_error(None, 'Vous ne pouvez pas désactiver ou rétrograder votre propre compte administrateur.')
        else:
            form.save()
            messages.success(request, 'Utilisateur modifié avec succès.')
            return redirect('utilisateurs:liste')
    return render(request, 'utilisateurs/modifier.html', {'form': form, 'user_obj': user_obj})


@administrateur_requis
def supprimer(request, pk):
    user_obj = get_object_or_404(Utilisateur, pk=pk)
    if user_obj.pk == request.user.pk:
        messages.error(request, 'Vous ne pouvez pas supprimer votre propre compte.')
        return redirect('utilisateurs:liste')
    if request.method == 'POST':
        user_obj.delete()
        messages.success(request, 'Compte supprimé avec succès.')
        return redirect('utilisateurs:liste')
    return render(request, 'utilisateurs/supprimer.html', {'user_obj': user_obj})


@administrateur_requis
def desactiver(request, pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    user_obj = get_object_or_404(Utilisateur, pk=pk)
    if user_obj.pk == request.user.pk:
        messages.error(request, 'Vous ne pouvez pas désactiver votre propre compte.')
    else:
        user_obj.is_active = False
        user_obj.save(update_fields=['is_active'])
        messages.success(request, 'Compte désactivé.')
    return redirect('utilisateurs:liste')


@login_required
def profil(request):
    form = InformationsUtilisateurForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Votre profil a été mis à jour.')
        return redirect('profil')
    return render(request, 'comptes/profil.html', {'form': form})


@login_required
def mot_de_passe(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Votre mot de passe a été modifié.')
    else:
        messages.error(request, 'Mot de passe non modifié : ' + ' '.join(str(e) for errors in form.errors.values() for e in errors))
    return redirect('profil')
