from enum import Enum, auto
from typing import NamedTuple, Type, TypeVar

from app.common.models import BaseModel
from rest_framework import status
from rest_framework.serializers import Serializer


class RequestMethod(Enum):
    """
    Class to represent possible request methods for different APIs. The http notation (get, post, put, delete, patch)
    is used instead of drf generic notation (list, create, retrieve, update, destroy, partial_update), because
    POST method is not always about creating, and also there is no need to differentiate GET into retrieve and list,
    because the main purpose in which this class would be used doesn't require "list method" at all.
    """

    GET = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()
    PATCH = auto()


class SerializersWithoutBody(NamedTuple):
    output: Type[Serializer] = None
    response_status: str = status.HTTP_204_NO_CONTENT


class SerializersWithBody(NamedTuple):
    input: Type[Serializer] = None
    output: Type[Serializer] = None
    response_status: str = status.HTTP_204_NO_CONTENT


SerializerGroup = SerializersWithoutBody | SerializersWithBody

DjangoModel = TypeVar("DjangoModel", bound=BaseModel)
