from django.contrib import admin
from .models import Trainer,Comment

admin.site.register(Trainer)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('trainee', 'trainer', 'rating', 'approved', 'created_at')
    list_filter = ('approved', 'rating', 'created_at')
    search_fields = ('trainee__user__email', 'trainer__user__email', 'comment')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f"{updated} comment(s) approved.")
    approve_comments.short_description = "Approve selected comments"
