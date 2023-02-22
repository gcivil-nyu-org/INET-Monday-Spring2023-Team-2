from django.shortcuts import render

# Create your views here.

# ============================= Map ==================================

def map(request):
    context = {}
    return render(request, 'voluncheer/map.html', context)