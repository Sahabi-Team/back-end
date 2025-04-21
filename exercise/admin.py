from django.contrib import admin
from .models import ExerciseTag, MuscleGroup, Equipment, Exercise, ExerciseImage

class ExerciseImageInline(admin.TabularInline):
    model = ExerciseImage
    extra = 1

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty', 'workoutplaces')
    search_fields = ('name', 'description')
    filter_horizontal = ('tags', 'muscle_groups', 'equipments')
    inlines = [ExerciseImageInline]

@admin.register(ExerciseTag)
class ExerciseTagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ExerciseImage)
class ExerciseImageAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'image')
