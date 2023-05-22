"""swipe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.account.views import ConfirmEmailView
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView, ResendEmailVerificationView
from dj_rest_auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from swipe import settings
from users.views import ConfirmCongratulationView, BuilderRegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    # auth user
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/registration/user', RegisterView.as_view(), name='account_signup'),
    path('api/registration/builder', BuilderRegisterView.as_view(), name='account_signup_builder'),

    path('api/auth/verify-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('api/auth/confirm-email/<str:key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('api/auth/confirmation-congratulations/', ConfirmCongratulationView.as_view(), name='confirm_congratulations'),
    path('api/auth/login/', LoginView.as_view(), name='account_login'),
    path('api/auth/logout/', LogoutView.as_view(), name='account_logout'),
    path('api/auth/password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('api/auth/password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('api/auth/resend-email/', ResendEmailVerificationView.as_view(), name='account_resend_email'),
    # DEBUG TOOLBAR
    path('__debug__/', include('debug_toolbar.urls')),

    # SPECTACULAR
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # URLS APP
    path('api/v1/', include('residential.urls')),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('announcements.urls')),
    path('api/v1/', include('files.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
