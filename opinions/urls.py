from django.urls import path
from .views import TicketListView, TicketCreateUpdateView

urlpatterns = [
    path('', TicketListView.as_view(), name='ticket-list'),
    path('create/', TicketCreateUpdateView.as_view(), name='ticket-create'),
]
