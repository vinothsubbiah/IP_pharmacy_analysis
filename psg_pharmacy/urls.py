from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('details/', views.details, name='details'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('requests/', views.requests, name='requests'),
    path('alerts/', views.alerts, name='alerts'),
    path('alerts_info/', views.alerts_info, name='alerts_info'),
]