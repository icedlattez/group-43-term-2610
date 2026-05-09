from django.urls import path
from . import views

urlpatterns = [
    path('', views.owner_list, name='owner_list'),
    path('<int:id>/', views.owner_detail, name='owner_detail'),
    path('<int:id>/edit/', views.owner_edit, name='owner_edit'),
    path('owners/create/', views.owner_create, name='owner_create'),

    path('stalls/', views.stall_list, name='stall_list'),
    path('stalls/create/', views.stall_create, name='stall_create'),
    path('stalls/<int:id>/', views.stall_detail, name='stall_detail'),
    path('stalls/<int:id>/edit/', views.stall_edit, name='stall_edit'),
]