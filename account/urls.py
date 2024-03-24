from django.urls import path
from rest_framework_simplejwt.views import (
                                            TokenRefreshView,
                                            TokenBlacklistView)
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('blacklist/', TokenBlacklistView.as_view(), name='blocklist'),
    path('password-change/', views.PasswordChangeView.as_view(), name='password-change'),
    path('edit/', views.UserEditView.as_view(), name='edit'),
    path('dashboard/', views.DashBoardView.as_view(), name='dashboard'),
]