from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Added admin dashboard route
    path('signup/', views.signup_view, name='signup'),
    path('create_user/', views.create_user, name='create_user'),
    path('showcase_projects/', views.showcase_projects, name='showcase_projects'),
    path('login/', views.login_user, name='login'),  # Added login route
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),  # URL for dashboard
    path('logout/', views.logout_user, name='logout'),  # URL for logout
]

