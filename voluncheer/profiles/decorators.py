from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def volunteer_required(
    function=None,
    redirect_field_name=REDIRECT_FIELD_NAME,
    login_url="login",
):
    """Decorator for views that checks that the logged in user is a volunteer."""  # noqa: E501
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_volunteer,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def organization_required(
    function=None,
    redirect_field_name=REDIRECT_FIELD_NAME,
    login_url="login",
):
    """Decorator for views that checks that the logged in user is an organization."""  # noqa: E501
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_organization,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
