from abc import ABC, abstractmethod
from typing import Any

from app.common.types import (
    APISerializers,
    RequestMethod,
    SerializerGroup,
    SerializersWithBody,
)
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class BaseCustomAPIView(APIView, ABC):
    """
    Base class for specific http method abstract classes. Allows API to have only 1 http method.
    """

    serializer_classes: APISerializers = {}
    default_schema_config: dict
    request_method: RequestMethod

    @property
    def serializers(self) -> SerializerGroup:
        return getattr(self.serializer_classes, self.request_method.name.lower())


class PostAPIView(BaseCustomAPIView):
    """
    Abstract class for most cases of post APIs.
    """

    request_method = RequestMethod.POST

    @abstractmethod
    def perform_action(self, *args, **kwargs) -> Any:
        """
        Main action of the API.
        """
        pass

    def post(self, request: Request, *args, **kwargs) -> Response:
        post_serializers = self.serializers
        input_serializer = post_serializers.input
        output_serializer = post_serializers.output
        response_status = post_serializers.response_status

        service_data = {}

        if input_serializer is not None:
            serializer = input_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            service_data = serializer.validated_data

        result = self.perform_action(service_data)

        if output_serializer is not None:
            return Response(output_serializer(result).data, status=response_status)

        return Response(status=status.HTTP_204_NO_CONTENT)


def auto_extend_schema(http_method: RequestMethod) -> Any:
    def wrapper(cls: BaseCustomAPIView) -> Any:
        lowercase_method_name = http_method.name.lower()
        method = getattr(cls, lowercase_method_name)
        serializers: SerializersWithBody = getattr(cls.serializer_classes, lowercase_method_name)
        decorator = extend_schema(
            request=serializers.input if http_method != RequestMethod.GET else None,
            responses={serializers.response_status: serializers.output},
        )
        setattr(cls, method.__name__, decorator(method))
        return cls

    return wrapper
