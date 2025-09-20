from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('home.urls')),
    path('accounts/', include('accounts.urls')),
    path('announcements/', include('announcements.urls')),
    path('diary/', include('diary.urls')),
    path('events/', include('events.urls')),
    path('forum/', include('forum.urls')),
    path('materials/', include('materials.urls')),
    path('polls/', include('polls.urls')),
]
