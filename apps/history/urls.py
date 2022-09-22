from django.urls import path
from . import views

app_name = 'history'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('users/', views.UserLogsView.as_view(), name='users'),
    path('inventories/', views.InventoriesLogsView.as_view(), name='inventories'),
    path('purchases/', views.PurchasesLogsView.as_view(), name='purchases'),
    path('recover-users/<int:pk>/', views.UserRollbackView.as_view(), name='recover-users'),
    path('recover-inventories/<int:pk>/', views.InventoriesRollbackView.as_view(), name='recover-inventories'),
    path('recover-purchases/<int:pk>/', views.PurchasesRollbackView.as_view(), name='recover-purchases'),
    # path('profile/', views.ProfileView.as_view(), name='profile'),
]