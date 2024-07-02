from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
     path('profile/', views.profile, name='profile'),
      path('deposit/', views.deposit, name='deposit'),
    path('logout/', views.user_logout, name='user_logout'),
]