from django.contrib.auth import get_user_model
from django.db import models

from app.common.models import BaseModel

User = get_user_model()


class ProductList(BaseModel):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)


class ProductCategory(BaseModel):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    position_number = models.PositiveSmallIntegerField()


class Product(BaseModel):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    list = models.ForeignKey(ProductList, on_delete=models.SET_NULL, null=True)
    categories = models.ManyToManyField(ProductCategory, blank=True)
