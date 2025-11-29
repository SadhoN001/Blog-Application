from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('tag/create/', views.TagCreateView.as_view(), name='create_tag'),
    path('tag/<slug:slug>/', views.post_by_tag, name='post_by_tag'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('deshboard/', views.deshboard, name='deshboard'),
    path('post/<slug:slug>/', views.post_details, name='post_details'),
    
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name= 'login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
