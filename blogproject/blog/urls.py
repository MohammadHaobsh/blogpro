from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:id>/update/', views.update_post, name='update_post'),
    path('post/<int:id>/delete/', views.delete_post, name='delete_post'),
]
