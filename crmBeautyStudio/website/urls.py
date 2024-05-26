from django.urls import path
from . import views

urlpatterns = [
    #Базовые пути
    path('', views.home, name="home"),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),

    #Пути для клиентов
    path('clients/', views.clientsList, name='clients'),
    path('clients/record/<int:pk>/', views.record, name='record'),

    path('profile/', views.profile, name='profile'),

    #Пути для сервисов
    path('services/', views.servicesList, name='services'),
    path('services/service_detail/<int:pk>/', views.service_detail, name='service_detail'),
    path('service/<int:pk>/edit/', views.edit_service, name='edit_service'),
    path('service/create/', views.create_service, name='create_service'),
    path('services/delete/<int:pk>/', views.delete_service, name='delete_service'),
    path('services/toggle-availability/<int:pk>/', views.toggle_service_availability, name='toggle_service_availability'),
]
