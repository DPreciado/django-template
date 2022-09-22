"""djangoproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.urls import include, path
from apps.users import views as users_views
from django.contrib.admin.views.decorators import staff_member_required


# from exampleApp.views import IndexExample

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('apps.dashboard.urls')),
    path('inventario/', include('apps.exampleInventario.urls')),
    path('compras/', include('apps.examplePurchases.urls')),
    path('log/', include('apps.history.urls')),
    path('animals/', include('apps.drfexampleapp.urls')),
    
    # User and Registration urls
    path('', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('profile/', users_views.ProfileView.as_view(), name='profile'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/login.html'), name='logout'),
    path('register/', users_views.RegisterView.as_view(), name='register'),
    path('register-admin/', staff_member_required(users_views.RegisterViewAdmin.as_view()), name='registerAdmin'),

    path('forgot-password/', users_views.forgot_password, name='forgot-password'),
    path('users/', include('apps.users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Remember that the last line regarding file/image uploads must be changed for production purposes: 
# https://docs.djangoproject.com/en/4.0/howto/static-files/deployment/