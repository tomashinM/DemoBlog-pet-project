from functools import wraps

from drf_spectacular.utils import extend_schema, extend_schema_serializer
from rest_framework import serializers
from rest_framework.response import Response

WRAPPED_SERIALIZER_CACHE = {}


class BodyErrorSerializer(serializers.Serializer):
    body = serializers.ListField(child=serializers.CharField())


class ErrorSerializer(serializers.Serializer):
    errors = BodyErrorSerializer()


def wrap_response(field_name="data"):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            response = func(self, request, *args, **kwargs)
            if isinstance(response, Response):
                response.data = {field_name: response.data}
            return response

        return wrapper

    return decorator


def wrap_schema(field_name="data", many=False, partial=False):
    def decorator(
        request_serializer=None,
        response_serializer=None,
        success_status=200,
        error_statuses=[400, 401],
    ):
        def create_wrapped_serializer(base_serializer, many, partial):
            if base_serializer is None:
                return None

            cache_key = (base_serializer, field_name, many, partial)
            if cache_key in WRAPPED_SERIALIZER_CACHE:
                return WRAPPED_SERIALIZER_CACHE[cache_key]

            component_name = "{}Wrapped{}{}{}".format(
                field_name,
                base_serializer.__name__.replace("Serializer", ""),
                "List" if many else "",
                "Partial" if partial else "",
            )
            wrapped_serializer = type(
                "WrappedSerializer",
                (serializers.Serializer,),
                {field_name: base_serializer(many=many, partial=partial)},
            )
            extended = extend_schema_serializer(
                many=False, component_name=component_name
            )(wrapped_serializer)
            WRAPPED_SERIALIZER_CACHE[cache_key] = extended
            return extended

        RequestSerializer = create_wrapped_serializer(
            request_serializer, False, partial
        )
        ResponseSerializer = create_wrapped_serializer(
            response_serializer, many, False
        )

        def wrapper(func):
            schema_params = {}
            schema_params["request"] = RequestSerializer
            responses = {}
            responses[success_status] = ResponseSerializer

            if error_statuses:
                for status in error_statuses:
                    responses[status] = ErrorSerializer

            schema_params["responses"] = responses
            return extend_schema(**schema_params)(func)

        return wrapper

    return decorator
