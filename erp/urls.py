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
from system.views import user_views, common_views, communication_views, entity_views, translation_views, team_views, role_permission_views, dataset_views
from sales.views import customers_views, vendors_views, addresses_views, invoices_views, receipts_views, pricelists_views, orders_views, quotations_views, credits_views, cart_views, return_views
from rest_framework_simplejwt import views as jwt_views
from warehouse.views import products_views, general_views, route_views, operation_views
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from rest_framework.authtoken import views
from django.conf import settings
from django.conf.urls.static import static 
# from rest_framework_swagger.views import get_swagger_view

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="ERP System API",
        default_version='1.0.0',
        description="API documentation of App",
    ),
    public=True,
)

router = routers.DefaultRouter()
##****************************************SYSTEM APP URL'S****************************************##
router.register(r'users', user_views.UserViewSet)
router.register(r'tables', dataset_views.TableViewSet)
router.register(r'data', dataset_views.DataViewSet)
router.register(r'groups', user_views.GroupViewSet)
router.register(r'roles', role_permission_views.RoleViewSet)
router.register(r'permissions', role_permission_views.PermissionViewSet)
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
router.register(r'formsections', common_views.FormSectionViewSet)
router.register(r'communications', communication_views.CommunicationViewSet)
router.register(r'channels', communication_views.ChannelViewSet)
router.register(r'entities', entity_views.EntityViewSet)
router.register(r'translations', translation_views.TranslationViewSet)
router.register(r'teams', team_views.TeamViewSet)
##****************************************SALES APP URL'S****************************************##
router.register(r'customers', customers_views.CustomerViewSet)
router.register(r'vendors', vendors_views.VendorViewSet)
router.register(r'addresses', addresses_views.AddressViewSet)
router.register(r'invoices', invoices_views.SalesInvoicesViewSet)
router.register(r'receipts', receipts_views.ReceiptsViewSet)
router.register(r'price_lists', pricelists_views.SalesPriceListsViewSet)
router.register(r'orders', orders_views.SalesOrdersViewSet)
router.register(r'order_lines', orders_views.SalesOrderLinesViewSet)
router.register(r'quotations', quotations_views.SalesQuotationsViewSet)
router.register(r'credits', credits_views.SalesCreditsViewSet)
router.register(r'carts', cart_views.CartsViewSet)
router.register(r'cart_lines', cart_views.CartlinesViewSet)
router.register(r'returns', return_views.SalesReturnsViewSet)
router.register(r'return_lines', return_views.SalesReturnLinesViewSet)
##****************************************PURCHASING APP URL'S****************************************##
##****************************************WAREHOUSE APP URL'S****************************************##
router.register(r'products', products_views.ProductViewSet)
router.register(r'product_locations', products_views.ProductLocationsViewSet)
router.register(r'product_counts', products_views.ProductCountsViewSet)
router.register(r'locations', products_views.LocationsViewSet)
#router.register(r'bom', products_views.BOMViewSet)
router.register(r'values', products_views.ValueViewSet)
router.register(r'uom', products_views.UOMViewSet)
router.register(r'journals', general_views.JournalViewSet)
router.register(r'journal_templates', general_views.JournalTemplateViewSet)
router.register(r'attributes', general_views.AttributeViewSet)
router.register(r'images', general_views.ImagesViewSet)
router.register(r'routes', route_views.Route_ViewSet)
router.register(r'route_types', route_views.Route_Type_ViewSet)
router.register(r'route_type_rules', route_views.Route_Type_Rules_ViewSet)
router.register(r'operations', operation_views.Operation_ViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
    path('api/', include(router.urls)),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token-verify/', jwt_views.TokenVerifyView.as_view(), name='verify_token'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)