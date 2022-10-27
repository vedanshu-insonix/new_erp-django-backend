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
from system.views import user_views, common_views, communication_views, company_views, translation_views
from sales.views import customers_views, vendors_views, addresses_views
from rest_framework_simplejwt import views as jwt_views
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from rest_framework.authtoken import views
from rest_framework_swagger.views import get_swagger_view

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
router.register(r'customers', customers_views.CustomerViewSet)
router.register(r'vendors', vendors_views.VendorViewSet)
router.register(r'addresses', addresses_views.AddressViewSet)
router.register(r'menus', common_views.MenuViewSet)
router.register(r'lists', common_views.ListViewSet)
router.register(r'columns', common_views.ColumnsViewSet)
router.register(r'forms', common_views.FormViewSet)
router.register(r'formlists', common_views.FormListViewSet)
router.register(r'formdata', common_views.FormDataViewSet)
# router.register(r'fields', common_views.FieldViewSet)
router.register(r'currencies', common_views.CurrencyViewSet)
router.register(r'tags', common_views.TagViewSet)
router.register(r'languages', common_views.LanguageViewSet)
router.register(r'countries', common_views.CountryViewSet)
router.register(r'states', common_views.StateViewSet)
router.register(r'stages', common_views.StageViewSet)
router.register(r'buttons', common_views.ButtonViewSet)
router.register(r'configurations', common_views.ConfigurationViewSet)
router.register(r'territories', common_views.TerritoriesViewSet)
router.register(r'choices', common_views.ChoiceViewSet)
router.register(r'helps', common_views.HelpViewSet)
router.register(r'formdata', common_views.FormDataViewSet)
router.register(r'formlist', common_views.FormListViewSet)
router.register(r'communications', communication_views.CommunicationViewSet)
router.register(r'channels', communication_views.ChannelViewSet)
router.register(r'companies', company_views.CompanyViewSet)
router.register(r'translations', translation_views.TranslationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/v1/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
    path('api/', include(router.urls)),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token-verify/', jwt_views.TokenVerifyView.as_view(), name='verify_token'),
]
