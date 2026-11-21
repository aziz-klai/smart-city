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
    path('ajouter/', CreateBatiment.as_view(), name='ajouter_batiment'),
    path('<int:pk>/', DetailBatiment.as_view(), name='detail_batiment'),
    path('<int:pk>/modifier/', UpdateBatiment.as_view(), name='modifier_batiment'),
    path('<int:pk>/supprimer/', DeleteBatiment.as_view(), name='supprimer_batiment'),
]
