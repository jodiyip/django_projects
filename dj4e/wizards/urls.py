from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='wizards'),
    # path('', views.WizardList.as_view(), name='wizards'),
    path('main/create/', views.WizardCreate.as_view(), name='wizards_create'),
    path('main/<int:pk>/update/', views.WizardUpdate.as_view(), name='wizards_update'),
    path('main/<int:pk>/delete/', views.WizardDelete.as_view(), name='wizards_delete'),
    path('lookup/', views.HouseView.as_view(), name='house_list'),
    path('lookup/create/', views.HouseCreate.as_view(), name='house_create'),
    path('lookup/<int:pk>/update/', views.HouseUpdate.as_view(), name='house_update'),
    path('lookup/<int:pk>/delete/', views.HouseDelete.as_view(), name='house_delete'),
]