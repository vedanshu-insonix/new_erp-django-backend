"""erp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include

from django.urls import include, path
from rest_framework import routers
from system.views import user_views, common_views
from sales.views import views as sales_view
from rest_framework_simplejwt import views as jwt_views
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view


schema_view = swagger_get_schema_view(
    openapi.Info(
        title="ERP System API",
        default_version='1.0.0',
        description="API documentation of App",
    ),
    public=True,
)

router = routers.DefaultRouter()
router.register(r'users', user_views.UserViewSet)
router.register(r'groups', user_views.GroupViewSet)
router.register(r'customers', sales_view.CustomerViewSet)
router.register(r'addresses', sales_view.AddressViewSet)
router.register(r'vendors', sales_view.VendorViewSet)
router.register(r'currencies', common_views.CurrencyViewSet)
router.register(r'tags', common_views.TagViewSet)
router.register(r'languages', common_views.LanguageViewSet)
router.register(r'countries', common_views.CountryViewSet)
router.register(r'states', common_views.StateViewSet)
router.register(r'stages', common_views.StageViewSet)
router.register(r'configurations', common_views.ConfigurationViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
    path('api/', include(router.urls)),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
