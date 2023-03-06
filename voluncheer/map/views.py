from django.shortcuts import render


def map(request):
    context = {}
    return render(request, "voluncheer/map.html", context)
