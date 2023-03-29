from django.shortcuts import render,redirect
from django.contrib.auth.views import redirect_to_login
# Create your views here.
def chatroom(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect_to_login(request.path)
    context = {}
    return render(request, "voluncheer/chatroom.html", context)
