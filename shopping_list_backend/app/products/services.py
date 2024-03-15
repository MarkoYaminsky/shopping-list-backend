from typing import Optional

from app.common.services import update_instance
from app.products.exceptions import CannotUpdatePositionNumberError
from app.products.models import Product, ProductCategory, ProductList
from django.contrib.auth import get_user_model
from django.db.models import F, QuerySet

User = get_user_model()


def get_all_product_lists(*args, **kwargs) -> QuerySet[ProductList]:
    return ProductList.objects.filter(*args, **kwargs)


def get_all_products(*args, **kwargs) -> QuerySet[Product]:
    return Product.objects.filter(*args, **kwargs)


def get_all_product_categories(*args, **kwargs) -> QuerySet[ProductCategory]:
    return ProductCategory.objects.filter(*args, **kwargs).order_by("position_number")


def create_product_list(author: User, name: str, **kwargs) -> ProductList:
    return ProductList.objects.create(author=author, name=name, **kwargs)


def create_product(name: str, product_list: Optional[ProductList] = None, **kwargs) -> Product:
    categories_ids = kwargs.pop("categories_ids", None)
    product = Product.objects.create(name=name, list=product_list, **kwargs)
    if categories_ids is not None:
        categories = get_all_product_categories(id__in=categories_ids)
        product.categories.set(categories)
    return product


def offset_categories_positions() -> None:
    get_all_product_categories().update(position_number=F("position_number") + 1)


def create_product_category(name: str, **kwargs) -> ProductCategory:
    offset_categories_positions()
    return ProductCategory.objects.create(name=name, position_number=1, **kwargs)


def update_product_list(product_list: ProductList, **kwargs) -> None:
    update_instance(instance=product_list, data=kwargs)


def update_product(product: Product, **kwargs) -> None:
    update_instance(instance=product, data=kwargs)


def update_product_category(product_category: ProductCategory, **kwargs) -> None:
    if "position_number" in kwargs:
        raise CannotUpdatePositionNumberError
    update_instance(instance=product_category, data=kwargs)


def delete_product_list(product_list: ProductList) -> None:
    product_list.delete()


def delete_product(product: Product) -> None:
    product.delete()


def delete_product_category(product_category: ProductCategory) -> None:
    get_all_product_categories(position_number__gt=product_category.position_number).update(
        position_number=F("position_number") - 1
    )
    product_category.delete()


def add_products_to_list(product_list: ProductList, products_ids: list[str]) -> None:
    get_all_products(id__in=products_ids).update(list=product_list)


def reposition_categories(categories_in_order: list[str]) -> None:
    categories_to_id = {str(category.id): category for category in get_all_product_categories()}
    updated_categories = []
    for index, category_id in enumerate(categories_in_order, start=1):
        category = categories_to_id[category_id]
        category.position_number = index
        updated_categories.append(category)
    ProductCategory.objects.bulk_update(updated_categories, fields=("position_number",))
