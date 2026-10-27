from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('user/<str:username>/', views.guest, name='guest'),
]
