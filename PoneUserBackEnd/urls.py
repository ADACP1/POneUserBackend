"""PoneUserBackEnd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
#from django.contrib.auth.decorators import login_required
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="POneUserBackend API",
      default_version='v1',
      description="POneUserBackend End Points",
      terms_of_service="https://www.pone.com",
      contact=openapi.Contact(email="info@pone.com"),
      license=openapi.License(name="POne License"),
   ),
   public=True,
   #permission_classes=(permissions.AllowAny,),
   #permission_classes=(permissions.IsAuthenticated ,),
   permission_classes=(permissions.IsAdminUser,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name = 'schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc', cache_timeout=0), name = 'schema-redoc'),
    path('api/v1/core/',include('core.api.router')),
    path('api/v1/employees/',include('employees.api.router')),
    path('api/v1/companies/',include('companies.api.router')),
    path('api/v1/schedules/',include('schedules.api.router')),
    path('api/v1/clocks/',include('clocks.api.router'))        

]
