from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('weather/', views.weather_view, name='weather'),
    path('oauth/google/', views.oauth_setup_view, {'provider': 'google'}, name='google_setup'),
    path('oauth/github/', views.oauth_setup_view, {'provider': 'github'}, name='github_setup'),
    path('accounts/', include('allauth.urls')),
    path('', views.login_view, name='home'),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
