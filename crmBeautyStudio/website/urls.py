from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('clients/', views.clientsList, name='clients'),
    path('services/', views.servicesList, name='services'),
    path('profile/', views.profile, name='profile'),
    path('clients/record/<int:pk>/', views.record, name='record'),
    path('services/service_detail/<int:pk>/', views.service_detail, name='service_detail'),
    path('service/<int:pk>/edit/', views.edit_service, name='edit_service'),
]
