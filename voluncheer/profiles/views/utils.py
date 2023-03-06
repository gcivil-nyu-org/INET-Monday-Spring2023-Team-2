from django.contrib import messages

def activateEmail(user, to_email):
    messages.success(f'Dear <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and click on \
    the received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')