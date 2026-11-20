from django.contrib import admin
from .models import document
class DocumentAdmin(admin.ModelAdmin):
    
    list_display = ('id_doc', 'nom_doc', 'type_doc', 'date', 'categorie', 'statut','description')
    list_filter = ('statut', 'nom_doc', 'type_doc')
    search_fields = ('id_doc', 'type_doc', 'nom_doc')
    readonly_fields = ('created_at', 'updates_at')
    fieldsets = (
        ('Informations ', {
            'fields': ('id_doc', 'nom_doc', 'type_doc', 'date', 'categorie', 'statut','description')
        }),
        ('Horodatage', {
            'fields': ('created_at', 'updates_at'),
            'classes': ('collapse',),
        }),
    )
    
admin.site.register(document,DocumentAdmin)

# Register your models here.
