from django.urls import path
from .views import (
    BlogPageView, 
    BlogDetailView,
    BlogCreateView, 
    BlogUpdateView,
    BlogDeleteView,
)

urlpatterns = [
    path('', BlogPageView.as_view(), name='home'),
    path('posts/<int:pk>/edit/', BlogUpdateView.as_view(), name = 'post_edit'),
    path('posts/<int:pk>/delete/', BlogDeleteView.as_view(), name = 'post_delete'),
    path('posts/<int:pk>/', BlogDetailView.as_view(), name = 'post_detail'),
    path('posts/new/', BlogCreateView.as_view(), name='post_new')
]