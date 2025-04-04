from django.contrib import admin
from .models import WorkoutPlan, WorkoutExercise

@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ("trainer", "trainee", "created_at", "is_active")
    list_filter = ("is_active", "created_at")
    search_fields = ("trainer__user__username", "trainee__user__username")
    ordering = ("-created_at",)

@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ("workout_plan", "exercise", "sets", "reps", "duration")
    list_filter = ("workout_plan", "exercise")
    search_fields = ("workout_plan__trainer__user__username", "exercise__name")
