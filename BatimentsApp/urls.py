from django.urls import path

from .views import (
    CreateBatiment,
    DeleteBatiment,
    DetailBatiment,
    ListeBatiment,
    UpdateBatiment,
)

app_name = 'Batiments'

urlpatterns = [
    path('', ListeBatiment.as_view(), name='liste_batiment'),
    path('batiments/ajouter/', CreateBatiment.as_view(), name='ajouter_batiment'),
    path('batiments/<int:pk>/', DetailBatiment.as_view(), name='detail_batiment'),
    path('batiments/<int:pk>/modifier/', UpdateBatiment.as_view(), name='modifier_batiment'),
    path('batiments/<int:pk>/supprimer/', DeleteBatiment.as_view(), name='supprimer_batiment'),
]
