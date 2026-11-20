from django.contrib import admin
from .models import Evenement



class EvenementAdmin(admin.ModelAdmin):
    list_display = ('id_evenement', 'nom', 'type', 'lieu','statut')
    search_fields = ('id_evenement', 'nom')
    list_editable = ('statut', 'type')
    list_filter = ('statut', 'type')
    list_per_page = 5
    fieldsets = (
        ('Identification', {
            'fields': ('nom','description', 'date_heure','lieu','capacite')
        }),
        ('Statut et Type', {
            'fields': ('statut','type')
        }),
    )
admin.site.register(Evenement, EvenementAdmin)

# Register your models here.
