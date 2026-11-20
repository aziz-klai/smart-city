from .views import *
from django.urls import path
app_name = 'Evenement'
urlpatterns = [
    path('liste/', Liste_Evenement.as_view(), name='liste_evenement'),
    path('detail_evenement/<int:pk>/', Detail_Evenement.as_view(), name='detail_evenement'),
    path('delete/<int:pk>/', Delete_Evenement.as_view(), name='delete_evenement'),
    path('create/', Create_Evenement.as_view(), name='create_evenement'),
    path('update/<int:pk>/', Update_Evenement.as_view(), name='update_evenement'),
]
