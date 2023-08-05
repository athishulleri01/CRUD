from django.urls import path
from . import views

urlpatterns = [
    path('', views.Loginpage, name='loginpage'),
    path('signup/', views.SignupPage, name='signup'),
    path('home/', views.HomePage, name='home'),
    path('user_logout/', views.LogoutPage, name='user_logout'),
]
