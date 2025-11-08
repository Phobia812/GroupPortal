from django.urls import path
from .views import (
    AnnouncementListView, AnnouncementDetailView, AnnouncementCreateView,
    AnnouncementUpdateView, AnnouncementDeleteView, AnnouncementJsonView
)

app_name = "announcements"

urlpatterns = [
    path('', AnnouncementListView.as_view(), name='list'),
    path('<int:pk>/', AnnouncementDetailView.as_view(), name='detail'),
    path('create/', AnnouncementCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', AnnouncementUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', AnnouncementDeleteView.as_view(), name='delete'),
    path('json/', AnnouncementJsonView.as_view(), name='json'),
]
