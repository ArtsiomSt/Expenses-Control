from django.contrib import admin
from django.urls import path, include, re_path
from mainpages.views import LinkUserFromTg

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainpages.urls')),
    path('api/v1/auth', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/linktg', LinkUserFromTg.as_view())
]
