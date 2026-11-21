from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'utilisateurs'
urlpatterns = [
    path('', LoginView.as_view(template_name='comptes/login.html'), name='connexion'),
    path('inscription/', views.inscription, name='inscription'),
    path('deconnexion/', LogoutView.as_view(), name='deconnexion'),
    path('profil/', views.profil, name='profil'),
    path('profil/mot-de-passe/', views.mot_de_passe, name='mot_de_passe'),
    path('profil/desactiver/', views.desactiver_mon_compte, name='desactiver_mon_compte'),
    path('gestion/', views.liste, name='liste'),
    path('gestion/ajouter/', views.ajouter, name='ajouter'),
    path('gestion/<int:pk>/', views.detail, name='detail'),
    path('gestion/<int:pk>/modifier/', views.modifier, name='modifier'),
    path('gestion/<int:pk>/supprimer/', views.supprimer, name='supprimer'),
    path('gestion/<int:pk>/desactiver/', views.desactiver, name='desactiver'),
]
