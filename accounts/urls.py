from django.urls import path
from .views import logout_view, RegisterView, LoginView, ActivateView, ProfileView

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("activate/<uidb64>/<token>/", ActivateView.as_view(), name="activate"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
