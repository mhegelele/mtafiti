from django.conf.urls import url, include
from django.contrib import admin

from mtafiti import views

urlpatterns = [
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/logout/$', views.logout, name='logout'),
    url(r'^', include('publications.urls')),
    url(r'^admin/', admin.site.urls),
]
