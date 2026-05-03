from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts import views as account_views
from events import views as event_views
from vendor import views as vendor_views

urlpatterns = [
    # ================= ADMIN =================
    path('admin/', admin.site.urls),

    # ================= AUTH & PROFILE =================
    path('', account_views.login_view, name='login'),
    path('signup/', account_views.signup_view, name='signup'),
    path('logout/', account_views.logout_view, name='logout'),
    path('profile/', account_views.profile_view, name='profile'),
    path('profile/request-organizer/', account_views.request_organizer_view, name='request_organizer'),
    path('profile/approve/<int:user_id>/', account_views.approve_organizer_view, name='approve_organizer'),
    path('profile/reject/<int:user_id>/', account_views.reject_organizer_view, name='reject_organizer'),

    # ================= HOME =================
    path('home/', event_views.event_list, name='home'),

    # ================= EVENTS =================
    path('event/create/', event_views.create_event, name='create_event'),
    path('event/<int:pk>/', event_views.event_detail, name='event_detail'),
    path('event/<int:pk>/register/', event_views.register_event, name='register_event'),
    path('event/<int:pk>/edit/', event_views.edit_event, name='edit_event'),

    # ================= DASHBOARD =================
    path('dashboard/', event_views.dashboard, name='dashboard'),

    # ================= VENDOR =================
    path('vendor/', vendor_views.vendor_list, name='vendor_list'),
    path('vendor/<int:id>/', vendor_views.vendor_detail, name='vendor_detail'),
    path('vendor/<int:id>/edit/', vendor_views.vendor_edit, name='vendor_edit'),

    # ================= STALLS =================
    path('stalls/', vendor_views.stall_list, name='stall_list'),
    path('stalls/create/', vendor_views.stall_create, name='stall_create'),
    path('stalls/<int:id>/edit/', vendor_views.stall_edit, name='stall_edit'),

    # ================= LISTINGS =================
    path('listings/', include('listings.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)