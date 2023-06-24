from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^api/v1/register$', views.register),
    url(r'^api/v1/login$', views.login),
    url(r'^api/v1/users$', views.handle_users),
    url(r'^api/v1/requests$', views.handle_requests),
    url(r'^api/v1/rides$', views.handle_rides)
]
