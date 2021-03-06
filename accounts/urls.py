from unicodedata import name
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(), name="login"),
    path('login/', views.user_login, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('register/', views.register, name="register"),

    #password change
    path('password_change/', auth_views.PasswordChangeView.as_view(), name="password_change"),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),

    #password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), 
            name="password_reset_confirm"),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path('profile/', views.profile, name="profile")
]