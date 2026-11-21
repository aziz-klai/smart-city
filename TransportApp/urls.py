from django.urls import path
from . import views

app_name = 'Transport'

urlpatterns = [
    path('', views.liste_transports, name='liste_transports'),
    path('ajouter/', views.ajouter_transport, name='ajouter_transport'),
    path('modifier/<int:id>/', views.modifier_transport, name='modifier_transport'),
    path('supprimer/<int:id>/', views.supprimer_transport, name='supprimer_transport'),
]