from django.contrib.auth.views import login as django_login
from django.contrib.auth.views import logout as django_logout


def login(request, template_name='publications/login.html'):
    return django_login(request, **{'template_name': template_name})


def logout(request, next_page='/accounts/login/', template_name='publications/login.html'):
    return django_logout(request, **{'next_page': next_page, 'template_name': template_name})
