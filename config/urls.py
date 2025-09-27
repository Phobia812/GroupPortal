from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)