from django.urls import path
from .views import ChatHistoryView, UnreadMessagesView

urlpatterns = [
    path('<int:mentorship_id>/history/', ChatHistoryView.as_view(), name='chat-history'),
    path('unread-messages/', UnreadMessagesView.as_view(), name='unread-messages')
]
