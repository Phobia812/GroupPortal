from django.http import HttpResponse
from django.urls import path

app_name = "events"

urlpatterns = [
    path('', lambda request: HttpResponse("Заглушка"), name='index'),
]