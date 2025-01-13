from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Admin-specific routes
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard route
    
    # User authentication and account management
    path('signup/', views.signup_user, name='signup'),
    path('login/', views.login_user, name='login'),  # Login route
    path('logout/', views.logout_user, name='logout'),  # Logout URL
    
    # Dashboard and project management
    path('dashboard/', views.dashboard, name='dashboard'),  # User dashboard
    path('upload_project/', views.upload_project, name='upload_project'),  # AJAX project upload
    path('project/edit/<int:project_id>/', views.edit_project, name='edit_project'),  # Edit project
    
    # Profile routes
    path('profile/upload-photo/', views.upload_photo, name='upload_photo'),  # Profile photo upload
    path('update_profile/', views.update_profile, name='update_profile'),  # Profile update route
    
    # Showcase and public-facing features
    path('showcase_projects/', views.showcase_projects, name='showcase_projects'),
    path('showcase/', views.showcase, name='showcase'),
    
    # Contact page
    path('contact/', views.contact, name='contact'),
    
    # Utility and system-level
    path('check-db-connection/', views.check_db_connection, name='check_db_connection'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
