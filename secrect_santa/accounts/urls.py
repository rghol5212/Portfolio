from django.urls import path

from . import views


app_name = "acc"


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('santas_list_signup/', views.santas_list_signup, name='santas_list_signup'),
    path('santascontrol/', views.santascontrol, name= 'santascontrol'),
]