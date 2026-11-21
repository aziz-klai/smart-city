from django.contrib import admin
from .models import Batiment


class BatimentAdmin(admin.ModelAdmin):
    list_display = ('id_batiment', 'nom', 'type', 'adresse', 'capacite', 'etat')
    search_fields = ('id_batiment', 'nom', 'adresse')
    list_editable = ('etat', 'type')
    list_filter = ('etat', 'type')
    list_per_page = 5
    fieldsets = (
        ('Identification', {
            'fields': ('nom', 'type', 'adresse', 'description')
        }),
        ('Informations pratiques', {
            'fields': ('capacite', 'horaires', 'etat', 'date')
        }),
    )


admin.site.register(Batiment, BatimentAdmin)