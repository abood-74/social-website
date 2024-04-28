from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    path('create/', views.ImageCreateAPIView.as_view(), name='create'),
    path('detail/<int:id>/', views.ImageDetailAPIView.as_view(), name='detail'),
    path('', views.ImageListAPIView.as_view(), name='list'),
    path('like/', views.ImageLikeAPIView.as_view(), name='like'),
    path('ranking/', views.ImageRankingAPIView.as_view(), name='ranking'),
]
    