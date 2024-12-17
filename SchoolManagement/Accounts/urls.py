from django.urls import path
from . views import *
urlpatterns = [
    path('',CommonloginView.as_view()),
   
]
