
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('auth/login/', LoginView.as_view(), name='account_login'),
    # path('auth/logout/', LogoutView.as_view(), name='account_logout'),
    # path('auth/registration/', RegisterView.as_view(), name='account_signup'),
    # path('auth/password/change/', PasswordChangeView.as_view(), name='password_change'),
    # path('auth/password-reset/', PasswordResetView.as_view(), name='password_reset'),
    # path('auth/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    # path('auth/resend-email/', ResendEmailVerificationView.as_view(), name='account_resend_email'),
    # path('auth/verify-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    # path('auth/confirm-email/<str:key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
    # path('auth/password-reset/confirm/<str:uid>/<str:token>/', UserResetPasswordConfirmView.as_view(),name='password_reset_confirm'),
    # path('auth/confirmation-congratulations/', ConfirmationCongratulationView.as_view(),name='confirmation_congratulations'),
]