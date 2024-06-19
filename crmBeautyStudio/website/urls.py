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

    #Пути для профиля
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    #Пути для сервисов
    path('services/', views.servicesList, name='services'),
    path('services/service_detail/<int:pk>/', views.service_detail, name='service_detail'),
    path('service/<int:pk>/edit/', views.edit_service, name='edit_service'),
    path('service/create/', views.create_service, name='create_service'),
    path('services/delete/<int:pk>/', views.delete_service, name='delete_service'),
    path('services/toggle-availability/<int:pk>/', views.toggle_service_availability, name='toggle_service_availability'),

    #Пути для блога
    path('news/', views.news_list, name='news_list'),
    path('news/<int:id>/', views.news_detail, name='news_detail'),
    path('news/add/', views.add_news, name='add_news'),
    path('news/edit/<int:id>/', views.edit_news, name='edit_news'),
    path('news/<int:id>/delete/', views.delete_news, name='delete_news'),

    #Пути для админа
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/register/', views.register_staff, name='register_staff'),
    path('staff/edit/<int:pk>/', views.edit_staff, name='edit_staff'),
    path('staff/delete/<int:pk>/', views.delete_staff, name='delete_staff'),
]
