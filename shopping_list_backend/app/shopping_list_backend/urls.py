from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

app_urls = [
    path("users/", include("app.users.urls", namespace="users")),
    path("products/", include("app.products.urls", namespace="products")),
]

management_urls = [
    path("admin/", admin.site.urls),
    path("schema/download/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

urlpatterns = [*management_urls, *app_urls]
