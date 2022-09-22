from django.urls import path
from . import views
from .api import views as api_views

app_name = 'animals'

urlpatterns = [
    path('api/', api_views.AnimalListCreateAPI.as_view(), name='api-list'),
    path('api/<int:pk>', api_views.AnimalDetails.as_view(), name='api-detail'),
    # path('', views.ViewPurchase.as_view(), name='index'),
    # path('profile/', views.ProfileView.as_view(), name='profile'),
]