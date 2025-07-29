from django.contrib import admin
from .models import Organizacion

@admin.register(Organizacion)
class OrganizacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'contacto_email', 'telefono', 'fecha_creacion')
    search_fields = ('nombre', 'contacto_email')
