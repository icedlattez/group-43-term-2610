from django.contrib import admin
HEAD
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vendor/', include('vendor.urls')),

from django.urls import path
from accounts import views as account_views
from events import views as event_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', account_views.login_view, name='login'),
    path('signup/', account_views.signup_view, name='signup'),
    path('home/', event_views.event_list, name='home'),
    path('logout/', account_views.logout_view, name='logout'),
181833fd93080f1105a285740f2eb301da16433d
]