from django.urls import path
from . import views

urlpatterns = [

    # VENDOR
    path('vendor/', views.vendor_list, name='vendor_list'),
    path('vendor/<int:id>/', views.vendor_detail, name='vendor_detail'),
    path('vendor/<int:id>/edit/', views.vendor_edit, name='vendor_edit'),

    # STALL
    path('stalls/', views.stall_list, name='stall_list'),
    path('stalls/create/', views.stall_create, name='stall_create'),
    path('stalls/<int:id>/edit/', views.stall_edit, name='stall_edit'),
    path('stalls/', views.stall_list, name='stall_list'),
    path('stalls/dashboard/', views.stall_dashboard, name='stall_dashboard'),
]
