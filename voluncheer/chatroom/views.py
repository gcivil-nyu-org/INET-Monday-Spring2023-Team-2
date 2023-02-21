from django.shortcuts import render

# Create your views here.

# ========================== Chatroom ================================

def chatroom_user(request, user_id):
    context = {}
    return render(request, 'voluncheer/chatroom.html', context)

def chatroom_organ(request, organ_id):
    context = {}
    return render(request, 'voluncheer/chatroom.html', context)