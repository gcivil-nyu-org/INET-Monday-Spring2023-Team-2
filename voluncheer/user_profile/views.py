from django.shortcuts import render, get_object_or_404

from .models import *
# Create your views here.

# ======================== User Profile ============================

def user_profile(request, user_id):
    user_profile = get_object_or_404(User, pk=user_id)
    badge_urls = []
    badge_list = user_profile.user_badges.split(",")
    for badge in badge_list:
        try:
            badge_urls.append(GLOBAL_BADGES[badge])
        except:
            pass
    context = {'user_profile': user_profile, 'badge_urls': badge_urls}
    return render(request, 'voluncheer/user_profile.html', context)