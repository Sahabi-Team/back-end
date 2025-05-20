from django.contrib import admin
from .models import Test

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('trainee', 'gender', 'body_form', 'goal', 'equipment', 'fitness_level', 'focus_area', 'created_at')
    list_filter = ('gender', 'goal', 'fitness_level', 'equipment', 'focus_area')
    search_fields = ('trainee__user__username', 'goal', 'focus_area')

