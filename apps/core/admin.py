from django.contrib import admin
from core.models import *


# Cliente.
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    list_filter= ('nome',)
    search_fields = ['nome']


    class Meta:
        model = Cliente