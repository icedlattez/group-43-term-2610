from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts import views as account_views
from events import views as event_views
from owner import views as owner_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # ================= AUTH =================
    path('', account_views.login_view, name='login'),
    path('signup/', account_views.signup_view, name='signup'),
    path('logout/', account_views.logout_view, name='logout'),
    path('profile/', account_views.profile_view, name='profile'),

    # ================= EVENTS =================
    path('home/', event_views.event_list, name='home'),
    path('dashboard/', event_views.dashboard, name='dashboard'),
    path('event/create/', event_views.create_event, name='create_event'),
    path('event/<int:id>/', event_views.event_detail, name='event_detail'),
    path('event/<int:id>/edit/', event_views.edit_event, name='edit_event'),
    path('event/<int:id>/register/', event_views.register_event, name='register_event'),

    # ================= OWNER =================
    path('owners/', owner_views.owner_list, name='owner_list'),
    path('owners/<int:id>/', owner_views.owner_detail, name='owner_detail'),
    path('owners/<int:id>/edit/', owner_views.owner_edit, name='owner_edit'),
    path('owners/', owner_views.owner_list, name='owner_list'),


    # ================= STALL =================
    path('stalls/', owner_views.stall_list, name='stall_list'),
    path('stalls/create/', owner_views.stall_create, name='stall_create'),
    path('stalls/<int:id>/', owner_views.stall_detail, name='stall_detail'),
    path('stalls/<int:id>/edit/', owner_views.stall_edit, name='stall_edit'),
    path('stalls/', owner_views.stall_list, name='stall_list'),

    # ================= PRODUCTS =================
    path('products/', include('products.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)