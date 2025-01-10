from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard route
    path('signup/', views.signup_user, name='signup'),
    path('showcase_projects/', views.showcase_projects, name='showcase_projects'),
    path('login/', views.login_user, name='login'),  # Login route
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard URL
    path('logout/', views.logout_user, name='logout'),  # Logout URL
    path('upload_project/', views.upload_project, name='upload_project'),
    path('showcase/', views.showcase, name='showcase'),
    path('check-db-connection/', views.check_db_connection, name='check_db_connection'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
