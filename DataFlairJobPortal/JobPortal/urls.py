from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('login/',loginUser,name='login'),
    path('logout/',logoutUser,name='logout'),
    path('plot/',plotData, name='plot'),
    path('register/',registerUser,name='register'),
    path('apply/',applyPage,name='apply'),
    
]