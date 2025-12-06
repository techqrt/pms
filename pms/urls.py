"""
URL configuration for pms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from pms_apps.authentication.urls import urlpatterns as auth_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(), name='redoc'),
# ----------------------------
    # # Core Auth & Users
    # # ----------------------------
    path('auth/',include('pms_apps.authentication.urls')),

    # # ----------------------------
    # # Department Modules
    # # ----------------------------
    path('lead/',include('pms_apps.lead.urls')),
    path('marketing/', include('pms_apps.marketing.urls')),
    path('property/', include('pms_apps.property.urls')),
    path('maintenance/', include('pms_apps.maintenance.urls')),
    # path('reception/', include('pms_apps.reception.urls')),
    # path('finance/', include('pms_apps.finance.urls')),
    # path('collection/', include('pms_apps.collection.urls')),
    # path('legal/', include('pms_apps.legal.urls')),
    # path('it/', include('pms_apps.IT.urls')),
    # path('agreement-team/', include('pms_apps.agreement_team.urls')),
    # path('owner/', include('pms_apps.owner.urls')),
    # path('general-manager/', include('pms_apps.general_manager.urls')),
]

# ----------------------------
# Static and Media (for Dev)
# ----------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
