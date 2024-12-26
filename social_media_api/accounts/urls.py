from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    re_path(r"^auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$", views.CustomConfirmEmailView.as_view(),name="account_confirm_email",),
    path("change-email/", views.ChangeEmailAPIView.as_view(), name="change-email"),
    path("password/resets/", views.PasswordResetAPIView.as_view(), name="api_password_reset"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
