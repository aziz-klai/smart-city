from django.urls import path
from .views import (
    Create_Document,
    Delete_Document,
    Detail_Document,
    Liste_Document,
    Update_Document,
)

app_name = 'Document'
urlpatterns = [
    path('', Liste_Document.as_view(), name='index'),
    path('list/', Liste_Document.as_view(), name='listdocument'),
    path('detail/<int:pk>/', Detail_Document.as_view(), name='detaildocument'),
    path('deletedocument/<int:pk>/', Delete_Document.as_view(), name='deletedocument'),
    path('createdocument/', Create_Document.as_view(), name='createdocument'),
    path('updatedocument/<int:pk>/', Update_Document.as_view(), name='updatedocument'),
]
