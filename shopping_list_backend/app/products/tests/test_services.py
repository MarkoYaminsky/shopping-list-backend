import pytest
from app.products.exceptions import CannotUpdatePositionNumberError
from app.products.models import Product, ProductCategory, ProductList
from app.products.services import (
    add_products_to_list,
    create_product,
    create_product_category,
    create_product_list,
    delete_product,
    delete_product_category,
    delete_product_list,
    offset_categories_positions,
    reposition_categories,
    update_product_category,
)
from app.products.tests.factories import (
    ProductCategoryFactory,
    ProductFactory,
    ProductListFactory,
)

pytestmark = pytest.mark.django_db


class TestCreateProductList:
    name = "Honey"

    def test_created(self, user):
        product_list = create_product_list(name=self.name, author=user)

        assert ProductList.objects.count() == 1
        assert ProductList.objects.first() == product_list
        assert product_list.name == self.name
        assert product_list.author == user


class TestCreateProduct:
    name = "Honey"

    def test_created(self, product_category):
        product = create_product(name=self.name, categories_ids=[product_category.id])

        assert Product.objects.count() == 1
        assert Product.objects.first() == product
        assert product.name == self.name
        assert product.categories.first() == product_category


class TestOffsetCategoriesPositions:
    def test_successful(self):
        second_category = ProductCategoryFactory.create(position_number=1)
        third_category = ProductCategoryFactory.create(position_number=2)
        fourth_category = ProductCategoryFactory.create(position_number=3)

        offset_categories_positions()

        for category in (second_category, third_category, fourth_category):
            category.refresh_from_db()
        assert second_category.position_number == 2
        assert third_category.position_number == 3
        assert fourth_category.position_number == 4


class TestCreateProductCategory:
    name = "Food"

    def test_created(self):
        second_category = ProductCategoryFactory.create(position_number=1)

        category = create_product_category(name=self.name)

        second_category.refresh_from_db()
        assert second_category.position_number == 2
        assert category.name == self.name
        assert category.position_number == 1
        assert ProductCategory.objects.count() == 2


class TestUpdateProductCategory:
    new_name = "Chemicals"

    def test_update_position_failed(self, product_category):
        with pytest.raises(CannotUpdatePositionNumberError):
            update_product_category(product_category=product_category, name=self.new_name, position_number=1)


class TestDeleteProductList:
    def test_deleted(self):
        product_list = ProductListFactory.create()

        delete_product_list(product_list)

        assert ProductList.objects.count() == 0


class TestDeleteProduct:
    def test_deleted(self):
        product = ProductFactory.create()

        delete_product(product)

        assert Product.objects.count() == 0


class TestDeleteProductCategory:
    def test_deleted(self):
        deleted_product_category = ProductCategoryFactory.create(position_number=1)
        first_product_category = ProductCategoryFactory.create(position_number=2)

        delete_product_category(deleted_product_category)

        first_product_category.refresh_from_db()
        assert ProductCategory.objects.count() == 1
        assert first_product_category.position_number == 1
        assert ProductCategory.objects.filter(id=deleted_product_category.id).exists() is False


class TestAddProductsToList:
    def test_added(self, product_list):
        products_ids = [product.id for product in ProductFactory.create_batch(size=2)]
        non_relevant_product = ProductFactory()

        add_products_to_list(product_list=product_list, products_ids=products_ids)

        products = Product.objects.filter(id__in=products_ids)
        assert products.filter(list=product_list).count() == products.count()
        assert non_relevant_product.list != product_list


class TestRepositionCategories:
    def test_repositioned(self):
        first_category = ProductCategoryFactory(position_number=3)
        second_category = ProductCategoryFactory(position_number=1)
        third_category = ProductCategoryFactory(position_number=2)

        reposition_categories(
            [str(category_id) for category_id in [first_category.id, second_category.id, third_category.id]]
        )

        for category in (first_category, second_category, third_category):
            category.refresh_from_db()
        assert first_category.position_number == 1
        assert second_category.position_number == 2
        assert third_category.position_number == 3
