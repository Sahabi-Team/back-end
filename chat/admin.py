from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'mentorship',
        'sender',
        'receiver',
        'short_content',
        'timestamp',
        'seen',
        'seen_at',
    )
    list_filter = ('seen', 'timestamp', 'mentorship')
    search_fields = (
        'sender__username',
        'receiver__username',
        'content',
        'mentorship__id',
    )
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'

    def short_content(self, obj):
        return obj.content[:50]
    short_content.short_description = 'Message'
