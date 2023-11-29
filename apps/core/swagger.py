from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from apps.core.utils import BothHttpAndHttpsSchemaGenerator

SchemaView = get_schema_view(
    openapi.Info(
        title="Weather API",
        default_version="v1",
        description="Provides access to information about the weather in cities",
        terms_of_service="",
        contact=openapi.Contact(name="ithesand"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
    generator_class=BothHttpAndHttpsSchemaGenerator,
)
