from django.urls import include, path
from rest_framework import routers
from .views import views

router = routers.DefaultRouter()
router.register(r'api/users', views.UserViewSet)
router.register(r'api/groups', views.GroupViewSet)
router.register(r'api/customers', views.CustomerViewSet)

# Wire our API using automatic URL routing.
# Moreover, we can include login URLs for browsable APIs.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]