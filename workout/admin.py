from django.contrib import admin
from .models import WorkoutPlan, WorkoutExercise

@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'mentorship', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'description', 'mentorship__student__user__first_name', 'mentorship__trainer__user__first_name']


@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ['exercise', 'workout_plan', 'day', 'sets', 'reps', 'duration', 'order']
    list_filter = ['day', 'workout_plan']
    search_fields = ['exercise__name', 'description', 'workout_plan__name']
    ordering = ['workout_plan', 'day', 'order']
