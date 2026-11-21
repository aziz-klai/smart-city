"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import TemplateView
from BatimentsApp.views import ListeBatiment
from DocumentsApp.views import Liste_Document

urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name='dashboard.html')), name='dashboard'),
    path('batiments/', login_required(ListeBatiment.as_view()), name='batiments'),
    path('batiments/', include('BatimentsApp.urls')),
    path('documents/', login_required(Liste_Document.as_view()), name='documents'),
    path('admin/', admin.site.urls),
    path('documents/', include('DocumentsApp.urls')),
    path('evenements/', include('EvenementsApp.urls')),
    path('transports/', include('TransportApp.urls')),
    path('utilisateurs/', include('utilisateurs.urls')),
]
