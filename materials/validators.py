from rest_framework import serializers
from urllib.parse import urlparse
from rest_framework.exceptions import ValidationError

ALLOWED_DOMAIN = 'youtube.com'


def validate_youtube_url(value):
    """
    Разрешает только ссылки на youtube.com
    """
    parsed_url = urlparse(value)
    domain = parsed_url.netloc.lower()

    if ALLOWED_DOMAIN not in domain:
        raise serializers.ValidationError(
            f"Разрешены только ссылки на {ALLOWED_DOMAIN}"
        )
    return value


class YouTubeLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, data):
        value = data.get(self.field)
        if value:
            parsed_url = urlparse(value)
            domain = parsed_url.netloc.lower()
            if 'youtube.com' not in domain:
                raise ValidationError({self.field: "Разрешены только ссылки на youtube.com"})
