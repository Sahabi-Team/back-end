from django.contrib import admin
from .models import Opinion

@admin.register(Opinion)
class OpinionAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
