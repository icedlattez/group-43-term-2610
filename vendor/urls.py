from django.urls import path
from . import views

urlpatterns = [
    # ---------------- VENDOR ----------------
    path('', views.vendor_list, name='vendor_list'),
    path('<int:id>/', views.vendor_detail, name='vendor_detail'),
    path('<int:id>/edit/', views.vendor_edit, name='vendor_edit'),

    # ---------------- STALL ----------------
    path('stalls/', views.stall_list, name='stall_list'),
    path('stalls/create/', views.stall_create, name='stall_create'),
]