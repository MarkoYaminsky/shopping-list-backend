from typing import List

from factory import SubFactory, LazyFunction, Sequence
from factory.django import DjangoModelFactory
from faker import Faker

from app.products.models import ProductList, ProductCategory, Product
from app.products.services import get_all_product_categories
from app.users.tests.factories import UserFactory

fake = Faker()


class ProductListFactory(DjangoModelFactory):
    class Meta:
        model = ProductList

    author = SubFactory(UserFactory)
    name = Sequence(lambda x: f"{fake.user_name()}{x}")


class ProductCategoryFactory(DjangoModelFactory):
    class Meta:
        model = ProductCategory

    position_number = LazyFunction(
        lambda: getattr(get_all_product_categories().order_by("position_number").last(), "position_number", 0) + 1
    )
    name = Sequence(lambda x: f"{fake.user_name()}{x}")


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    list = SubFactory(ProductListFactory)
    name = Sequence(lambda x: f"{fake.user_name()}{x}")

    @classmethod
    def create(cls, categories: List[ProductCategory] = (), **kwargs) -> Product:
        product = super().create()
        product.categories.set(categories or [ProductCategoryFactory()])
        return product
