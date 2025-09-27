from django.urls import path
from . import views

urlpatterns = [
    path("", views.grade_list, name="grade_list"),
    path("create/", views.grade_add, name="grade_add"),
    path("update/<int:pk>/", views.grade_update, name="grade_update"),
    path("delete/<int:pk>/", views.grade_delete, name="grade_delete"),
]