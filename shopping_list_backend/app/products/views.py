from app.products.models import Product, ProductCategory, ProductList
from app.products.serializers import (
    ListProductOutputSerializer,
    ProductCategoryCreateInputSerializer,
    ProductCategoryListOutputSerializer,
    ProductCategoryRetrieveOutputSerializer,
    ProductCreateInputSerializer,
    ProductListCreateInputSerializer,
    ProductListOutputSerializer,
    ProductListRetrieveOutputSerializer,
    ProductRetrieveOutputSerializer,
)
from app.products.services import (
    create_product_category,
    create_product_list,
    delete_product,
    delete_product_category,
    delete_product_list,
    get_all_product_categories,
    get_all_product_lists,
    get_all_products,
    update_product,
    update_product_category,
    update_product_list,
)
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class ListCreateProductListAPI(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ListProductOutputSerializer

    def get(self, request):
        user = request.user
        user_product_lists = get_all_product_lists(author=user)
        return Response(self.serializer_class(user_product_lists).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductListCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_list = create_product_list(author=request.user, **serializer.validated_data)
        return Response(self.serializer_class(product_list).data, status=status.HTTP_201_CREATED)


class ProductListRetrieveUpdateDestroyAPI(APIView):
    serializer_class = ProductListRetrieveOutputSerializer

    def get_product_list(self, product_list_id) -> ProductList:
        return get_object_or_404(ProductList, id=product_list_id)

    def get(self, request, product_list_id):
        product_list = self.get_product_list(product_list_id)
        return Response(self.serializer_class(product_list).data, status=status.HTTP_200_OK)

    def patch(self, request, product_list_id):
        product_list = self.get_product_list(product_list_id)
        serializer = ProductListCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        update_product_list(product_list, **serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, product_list_id):
        product_list = self.get_product_list(product_list_id)
        delete_product_list(product_list)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListCreateAPI(ListAPIView):
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("category__name", "name")
    ordering_fields = ("category__name", "name")
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductListOutputSerializer

    def get(self, request, *args, **kwargs):
        user_product_lists = get_all_products()
        return Response(self.serializer_class(user_product_lists).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_list = create_product_list(author=request.user, **serializer.validated_data)
        return Response(self.serializer_class(product_list).data, status=status.HTTP_201_CREATED)


class ProductRetrieveUpdateDestroyAPI(APIView):
    serializer_class = ProductRetrieveOutputSerializer

    def get_product(self, product_id) -> Product:
        return get_object_or_404(Product, id=product_id)

    def get(self, request, product_id):
        product = self.get_product(product_id)
        return Response(self.serializer_class(product).data, status=status.HTTP_200_OK)

    def patch(self, request, product_id):
        product = self.get_product(product_id)
        serializer = ProductCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        update_product(product, **serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, product_id):
        product = self.get_product(product_id)
        delete_product(product)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductCategoryListCreateAPI(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductCategoryListOutputSerializer

    def get(self, request, *args, **kwargs):
        user_product_lists = get_all_product_categories()
        return Response(self.serializer_class(user_product_lists).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductCategoryCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_list = create_product_category(**serializer.validated_data)
        return Response(self.serializer_class(product_list).data, status=status.HTTP_201_CREATED)


class ProductCategoryUpdateDestroyAPI(APIView):
    serializer_class = ProductCategoryRetrieveOutputSerializer

    def get_product_category(self, product_id) -> ProductCategory:
        return get_object_or_404(ProductCategory, id=product_id)

    def get(self, request, product_id):
        product_category = self.get_product_category(product_id)
        return Response(self.serializer_class(product_category).data, status=status.HTTP_200_OK)

    def patch(self, request, product_id):
        product_category = self.get_product_category(product_id)
        serializer = ProductCategoryCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        update_product_category(product_category, **serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, product_id):
        product_category = self.get_product_category(product_id)
        delete_product_category(product_category)
        return Response(status=status.HTTP_204_NO_CONTENT)