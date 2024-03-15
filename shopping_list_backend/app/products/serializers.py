from app.products.models import Product, ProductList
from app.users.serializers import UserShortOutputSerializer
from rest_framework import serializers


class ListProductOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductList
        fields = ("id", "name")


class ProductListCreateInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductList
        fields = ("name", "description")


class ProductListRetrieveOutputSerializer(serializers.ModelSerializer):
    author = UserShortOutputSerializer()

    class Meta:
        model = ProductList
        fields = ("name", "description", "author")


class ProductListOutputSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name")

    class Meta:
        model = Product
        fields = ("id", "category_name", "name")


class ProductCreateInputSerializer(serializers.ModelSerializer):
    categories_ids = serializers.ListField(child=serializers.UUIDField(), required=False)

    class Meta:
        model = Product
        fields = ("name", "description", "categories_ids")


class ProductRetrieveOutputSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name")

    class Meta:
        model = Product
        fields = ("name", "description", "category_name")


class ProductCategoryListOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "description")


class ProductCategoryCreateInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "description")


class ProductCategoryRetrieveOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "description")
