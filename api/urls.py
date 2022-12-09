from django.urls import path
from .views import *


urlpatterns = [
    path('register',RegisterUser.as_view()),
    path('login',LoginUser.as_view()),
    path('user',Userview.as_view()),
    path('logout',LogoutUser.as_view()),
]
