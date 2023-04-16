from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    """Generic signup where users can select their user type."""

    template_name = "registration/signup.html"


def home(request):
    """Directs the user to their home page."""
    if request.user.is_authenticated:
        return redirect(f"profile/{request.user.pk}")
    return render(request, "voluncheer/home.html")
