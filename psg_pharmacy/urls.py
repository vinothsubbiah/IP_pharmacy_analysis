from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('signup',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('index',views.index,name='index'),
    path('orders',views.orders,name='orders'),
    path('ml_predict',views.ml_predict,name='ml_predict'),
    path("",views.messaiah,name="messaiah"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('get_orders/', views.get_orders, name='get_orders'),
    path('details/', views.details, name='details'),
    path('requests/', views.requests, name='requests'),
    path('alerts/', views.alerts, name='alerts'),
    path('mailCompose/', views.mailCompose, name='mailCompose'),
    path('sendMail/', views.sendMail, name='sendMail'),
    path('alerts_info/', views.alerts_info, name='alerts_info'),
    path('signout',views.signout,name='signout'),
    ]

    