from django.shortcuts import render

# Create your views here.

# ======================== Registration ============================
def registration(request):
  context = {}
  return render(request, 'voluncheer/registration.html', context)