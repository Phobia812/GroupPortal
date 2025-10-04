from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import UserProfile

from django.shortcuts import render
from accounts.models import UserProfile
from diary.models import Grade
from home.models import GroupInfo

def home_view(request):
    userprofile = None
    recent_grades = None

    if request.user.is_authenticated:
        try:
            userprofile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            userprofile = None

        recent_grades = Grade.objects.filter(student=request.user).order_by('-date')[:3]

        group_info = GroupInfo.get_active_info()

    context = {
        'userprofile': userprofile,
        'recent_grades': recent_grades if request.user.is_authenticated else None,
        'group_info': group_info if request.user.is_authenticated else None,
        'news_list': [],
        'forum_topics': [],
        'diary_entries': [],
        'events': [],
        'announcements': [],
        'materials': [],
        'polls': [],
    }

    return render(request, 'home/home.html', context)
