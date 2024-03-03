from abc import ABC, abstractmethod
from typing import Any, Type

from app.common.types import RequestMethod, SerializerGroup
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class BaseCustomAPIView(APIView, ABC):
    """
    Base class for specific http method abstract classes. Allows API to have only 1 http method.
    """

    serializer_classes: SerializerGroup
    default_schema_config: dict
    request_method: RequestMethod

    @abstractmethod
    def perform_action(self, *args, **kwargs) -> Any:
        """
        Main action of the API.
        """
        pass


class PostAPIView(BaseCustomAPIView, ABC):
    """
    Abstract class for most cases of post APIs.
    """

    request_method = RequestMethod.POST

    def post(self, request: Request, *args, **kwargs) -> Response:
        post_serializers = self.serializer_classes
        input_serializer = post_serializers.input
        output_serializer = post_serializers.output

        service_data = {}

        if input_serializer is not None:
            serializer = input_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            service_data = serializer.validated_data

        result = self.perform_action(**service_data)

        if output_serializer is not None:
            return Response(output_serializer(result).data, status=post_serializers.response_status)

        return Response(status=status.HTTP_204_NO_CONTENT)


class GetAPIView(BaseCustomAPIView, ABC):
    """
    Abstract class for most cases of get (retrieve) APIs.
    """

    request_method = RequestMethod.GET

    @abstractmethod
    def get_object(self, *args, **kwargs) -> Any:
        """Returns a raw object that will be processed in perform_action"""
        pass

    def perform_action(self, retrieved_object: Any, *args, **kwargs) -> Any:
        """Returns a processed object that would be serialized with output serializer."""
        return retrieved_object

    def get(self, request: Request, *args, **kwargs) -> Response:
        get_serializers = self.serializer_classes
        retrieved_object = self.get_object(*args, **kwargs)
        result = self.perform_action(retrieved_object)
        return Response(get_serializers.output(result).data, status=get_serializers.response_status)


class PutAPIView(BaseCustomAPIView, ABC):
    """
    Abstract class for most cases of put (update) APIs.
    """

    request_method = RequestMethod.PUT
    partial = False

    @abstractmethod
    def get_object(self, *args, **kwargs) -> Any:
        """Returns an object or queryset to be updated later in perform_action"""
        pass

    @abstractmethod
    def perform_action(self, update_object: Any, **kwargs) -> Any:
        pass

    def put(self, request: Request, *args, **kwargs) -> Response:
        put_serializers = self.serializer_classes
        input_serializer = put_serializers.input
        output_serializer = put_serializers.output
        response_status = put_serializers.response_status

        update_object = self.get_object()
        serializer = input_serializer(update_object, data=request.data, partial=self.partial)
        serializer.is_valid(raise_exception=True)
        service_data = serializer.validated_data

        result = self.perform_action(update_object, **service_data)

        if output_serializer is not None:
            return Response(output_serializer(result).data, status=response_status)

        return Response(status=status.HTTP_204_NO_CONTENT)


class PatchAPIView(PutAPIView, ABC):
    """
    Abstract class for most cases of patch (partial update) APIs.
    """

    request_method = RequestMethod.PATCH
    partial = True

    def patch(self, request: Request, *args, **kwargs) -> Response:
        return self.put(request, *args, **kwargs)


def auto_extend_schema(cls: Type[BaseCustomAPIView]) -> Any:
    http_method = cls.request_method
    lowercase_method_name = http_method.name.lower()
    method = getattr(cls, lowercase_method_name)
    serializers: SerializerGroup = cls.serializer_classes
    decorator = extend_schema(
        request=serializers.input if http_method != RequestMethod.GET else None,
        responses={serializers.response_status: serializers.output},
    )
    setattr(cls, method.__name__, decorator(method))
    return cls
