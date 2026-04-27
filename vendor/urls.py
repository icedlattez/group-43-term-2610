from django.urls import path
from . import views

urlpatterns = [
    # ================= VENDOR =================

    # all vendors
    path('vendor/', views.vendor_list, name='vendor_list'),

    # vendor detail
    path('vendor/<int:id>/', views.vendor_detail, name='vendor_detail'),

    # edit vendor
    path('vendor/<int:id>/edit/', views.vendor_edit, name='vendor_edit'),

    # 🔥 CREATE VENDOR UNDER EVENT (IMPORTANT NEW ROUTE)
    path('event/<int:event_id>/vendor/create/', views.create_vendor, name='create_vendor'),


    # ================= STALL =================

    # all stalls
    path('stalls/', views.stall_list, name='stall_list'),

    # create stall under vendor (IMPORTANT FIX)
    path('vendor/<int:vendor_id>/stall/create/', views.stall_create, name='stall_create'),

    # edit stall
    path('stalls/<int:id>/edit/', views.stall_edit, name='stall_edit'),


    # ================= HOME =================

    path('home/', views.home, name='home'),
]