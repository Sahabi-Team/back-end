from django.contrib import admin
from .models import Mentorship

@admin.register(Mentorship)
class MentorshipAdmin(admin.ModelAdmin):
    list_display = ('trainee', 'trainer', 'created_at', 'expires_at', 'is_active', 'is_expired')
    list_filter = ('is_active', 'created_at', 'expires_at')
    search_fields = ('trainee__user__username', 'trainer__user__username')
    readonly_fields = ('expires_at',)
    
    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Expired'
