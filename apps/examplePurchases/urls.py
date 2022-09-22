from django.urls import path
from . import views

app_name = 'examplePurchases'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('create/', views.Create.as_view(), name='create'),
    path('show/<int:pk>/', views.Show.as_view(), name='show'),
    path('edit/<int:pk>/', views.Edit.as_view(), name='edit'),
    path('delete/<int:pk>/', views.Delete.as_view(), name='delete'),
    path('deleteRelation/<int:pk>', views.DeleteRelation.as_view(), name='deleteRelation'),
]