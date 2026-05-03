from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/request-organizer/', views.request_organizer_view, name='request_organizer'),
    path('profile/approve/<int:user_id>/', views.approve_organizer_view, name='approve_organizer'),
]