from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

urlpatterns = [
    path('blog/', include('blog.urls')),
    path('search/', include('search.urls')),
    path('admin/', admin.site.urls),
]

# Swagger's ulr Configuration........

schema_view = get_schema_view(
    openapi.Info(
        title="Django-Drf-Elasticsearch",
        default_version='v1',
        description='This is for testing purpose though which i am trying to learn how its actually work in drf and '
                    'Django',
        contact=openapi.Contact(email='contact@openai.com'),
    ),
    public=True,
)

urlpatterns += [
    # Other URL patterns
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    path('redoc/', schema_view.with_ui('redoc'), name='schema-redoc'),
]
