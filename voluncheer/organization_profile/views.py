from django.shortcuts import render, get_object_or_404

from .models import *
# Create your views here.

# ==================== Organization Profile =========================

def organization_profile(request, organ_id):
    organ_profile = get_object_or_404(Organization, pk=organ_id)
    job_lists = organ_profile.job_set.all()
    context = {'organ_profile': organ_profile, 'job_lists': job_lists}
    return render(request, 'voluncheer/organization_profile.html', context)