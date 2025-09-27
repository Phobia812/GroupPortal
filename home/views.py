from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import UserProfile

def home_view(request):
    profile = None
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            profile = None
    return render(request, 'home/home.html', {
        'profile': profile
    })
