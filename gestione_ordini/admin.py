from django.contrib import admin
from gestione_ordini.models import File, Ordine, Profilo

# Register your models here.
admin.site.register(File)
admin.site.register(Ordine)
admin.site.register(Profilo)