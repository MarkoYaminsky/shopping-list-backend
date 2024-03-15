from app.products.views import (
    ListCreateProductListAPI,
    ProductCategoryListCreateAPI,
    ProductCategoryUpdateDestroyAPI,
    ProductListCreateAPI,
    ProductListRetrieveUpdateDestroyAPI,
    ProductRetrieveUpdateDestroyAPI,
)
from django.urls import path

app_name = "products"

urlpatterns = [
    path("", ProductListCreateAPI.as_view(), name="products-list-create"),
    path("<uuid:product_id>/", ProductRetrieveUpdateDestroyAPI.as_view(), name="products-get-update-delete"),
    path("lists/", ListCreateProductListAPI.as_view(), name="product-lists-list-create"),
    path(
        "lists/<uuid:product_list_id>/",
        ProductListRetrieveUpdateDestroyAPI.as_view(),
        name="product-lists-get-update-delete",
    ),
    path("categories/", ProductCategoryListCreateAPI.as_view(), name="product-categories-list-create"),
    path(
        "categories/<uuid:product_category_id>/",
        ProductCategoryUpdateDestroyAPI.as_view(),
        name="product-categories-get-update-delete",
    ),
]
