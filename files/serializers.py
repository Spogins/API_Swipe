from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from files.models import Photo


class GallerySerializer(serializers.ModelSerializer):
    pass


class PhotoSerializer(serializers.ModelSerializer):
    image = Base64ImageField(use_url=True)
    class Meta:
        model = Photo
        exclude = ['gallery', 'id']
