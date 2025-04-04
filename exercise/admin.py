from django.contrib import admin
from .models import Exercise, ExerciseTag, ExerciseImage

class ExerciseImageInline(admin.TabularInline):
    """Allows adding multiple images inside the Exercise admin page"""
    model = ExerciseImage
    extra = 1

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'description']
    filter_horizontal = ['tags']
    inlines = [ExerciseImageInline]  # Add images inline

@admin.register(ExerciseTag)
class ExerciseTagAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(ExerciseImage)
class ExerciseImageAdmin(admin.ModelAdmin):
    list_display = ['exercise', 'image']
