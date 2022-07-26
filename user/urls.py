# ~/user/urls.py

from django.urls import path
from .views import Login, Join, LogOut, UploadProfile
from content.views import Main


urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('join', Join.as_view(), name='join'),
    path('main', Main.as_view(), name='main'),
    path('logout', LogOut.as_view(), name="logout"),
    path('uploadprofile', UploadProfile.as_view(), name='uploadprofile')
]