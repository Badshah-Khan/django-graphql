from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from .schema import schema
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.PUBLIC_FOLDER_URL_PREFIX, document_root=settings.PUBLIC_FOLDER_PATH)