import pytest

from app.products.models import ProductList, ProductCategory, Product
from app.products.tests.factories import ProductListFactory, ProductCategoryFactory, ProductFactory


@pytest.fixture
def product_list() -> ProductList:
    return ProductListFactory.create()


@pytest.fixture
def product_category() -> ProductCategory:
    return ProductCategoryFactory.create()


@pytest.fixture
def product() -> Product:
    return ProductFactory.create()
