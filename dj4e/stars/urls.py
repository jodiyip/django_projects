from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='stars'),
    path('main/create/', views.StarCreate.as_view(), name='stars_create'),
    path('main/<int:pk>/update/', views.StarUpdate.as_view(), name='stars_update'),
    path('main/<int:pk>/delete/', views.StarDelete.as_view(), name='stars_delete'),
    path('lookup/', views.TypeView.as_view(), name='type_list'),
    path('lookup/create/', views.TypeCreate.as_view(), name='type_create'),
    path('lookup/<int:pk>/update/', views.TypeUpdate.as_view(), name='type_update'),
    path('lookup/<int:pk>/delete/', views.TypeDelete.as_view(), name='type_delete'),
]