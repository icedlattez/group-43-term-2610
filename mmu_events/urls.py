from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views
from events import views as event_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('vendor/', include('vendor.urls')),

    path('', account_views.login_view, name='login'),
    path('signup/', account_views.signup_view, name='signup'),
    path('home/', event_views.event_list, name='home'),
    path('logout/', account_views.logout_view, name='logout'),
]