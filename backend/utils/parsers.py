from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ParseError


def get_custom_parser(field_name):
    class CustomJSONParser(JSONParser):
        def parse(self, stream, media_type=None, parser_context=None):
            data = super().parse(stream, media_type, parser_context)
            if not isinstance(data, dict) or field_name not in data:
                raise ParseError(
                    f"Invalid data format. Expected {{{field_name}: ...}}"
                )
            return data[field_name]

    return CustomJSONParser
