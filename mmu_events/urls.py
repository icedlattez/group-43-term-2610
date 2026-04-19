from django.contrib import admin
from django.urls import path

from accounts import views as account_views
from events import views as event_views

urlpatterns = [
    # ---------------- ADMIN ----------------
    path('admin/', admin.site.urls),

    # ---------------- AUTH ----------------
    path('', account_views.login_view, name='login'),
    path('signup/', account_views.signup_view, name='signup'),
    path('logout/', account_views.logout_view, name='logout'),

    # ---------------- EVENT SYSTEM ----------------
    path('home/', event_views.event_list, name='home'),

    # IMPORTANT: static routes FIRST
    path('event/create/', event_views.create_event, name='create_event'),

    # dynamic route LAST (VERY IMPORTANT)
    path('event/<int:pk>/', event_views.event_detail, name='event_detail'),

    # ---------------- DASHBOARD ----------------
    path('dashboard/', event_views.dashboard, name='dashboard'),
]