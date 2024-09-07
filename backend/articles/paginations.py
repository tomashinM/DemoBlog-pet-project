from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class ArticlePagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100

    def get_paginated_response(self, data):
        return Response({"articles": data, "articlesCount": self.count})

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "required": ["articles", "articlesCount"],
            "properties": {
                "articlesCount": {
                    "type": "integer",
                },
                "articles": schema,
            },
        }
