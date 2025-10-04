from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls', namespace='home')),
    path('', include('accounts.urls', namespace='accounts')),
    path('announcements/', include('announcements.urls', namespace='announcements')),
    path('diary/', include('diary.urls', namespace='diary')),
    path('events/', include('events.urls', namespace='events')),
    path('forum/', include('forum.urls', namespace='forum')),
    path('materials/', include('materials.urls', namespace='materials')),
    path('polls/', include('polls.urls', namespace='polls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)