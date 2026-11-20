from .views import *
from django.urls import path
app_name = 'Document'
urlpatterns = [
    
    path('list/', Liste_Document.as_view(), name='listdocument'),
    path('detail/<int:pk>/', Detail_Document.as_view(), name='detaildocument'),
    path('deletedocument/<int:pk>/', Delete_Document.as_view(), name='deletedocument'),
    path('createdocument/', Create_Document.as_view(), name='createdocument'),
    path('updatedocument/<int:pk>/', Update_Document.as_view(), name='updatedocument'),
]
