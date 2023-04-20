from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('login/',loginUser,name='login'),
    path('logout/',logoutUser,name='logout'),
    path('plot/',plotData, name='plot'),
    path('plotbar/',plotDataBar, name='plotbar'),
    path('register/',registerUser,name='register'),
    path('apply/',applyPage,name='apply'),
    path('search/',search,name='search'),
    path('applyfilter/',applyFilter,name='applyfilter'),
    
]