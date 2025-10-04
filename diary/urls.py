from django.urls import path
from .views import (
    GradeListView,
    GradeCreateView,
    GradeUpdateView,
    GradeDeleteView,
)

app_name = "diary"

urlpatterns = [
    path('', GradeListView.as_view(), name='grade_list'),
    path('create/', GradeCreateView.as_view(), name='grade_add'),
    path('<int:pk>/edit/', GradeUpdateView.as_view(), name='grade_update'),
    path('<int:pk>/delete/', GradeDeleteView.as_view(), name='grade_delete'),
]
