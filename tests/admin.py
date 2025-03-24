from django.contrib import admin
from .models import Test

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('trainee', 'goal', 'workout_room', 'workout_experience', 'created_at')
    list_filter = ('goal', 'workout_experience', 'workout_room')
    search_fields = ('trainee__user__username', 'goal')

