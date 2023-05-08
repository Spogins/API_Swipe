from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from files.models import Gallery, Photo
from files.serializers import PhotoSerializer
from residential.models import Complex
from users.serializers import AuthUserSerializer
from django.utils.translation import gettext_lazy as _


class ResidentialListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Complex
        fields = ['id', 'user', 'name', 'description']


class ResidentialSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(use_url=True)
    photo_gallery = PhotoSerializer(many=True, required=False)
    user = AuthUserSerializer(read_only=True)

    class Meta:
        model = Complex
        exclude = ['gallery']

    def create(self, validated_data):
        gallery = validated_data.pop('photo_gallery', None)
        res_complex = Complex.objects.create(
            user=self.context['request'].user,
            gallery=Gallery.objects.create(name='residential_complex'),
            **validated_data
        )

        if gallery:
            for elem in gallery:
                photo = Photo.objects.create(
                    image=elem.get('image'),
                    gallery=res_complex.gallery
                )
                photo.save()
        return res_complex

    def update(self, instance: Complex, validated_data):
        gallery = validated_data.pop('photo_gallery', None)

        for elem in validated_data.keys():
            setattr(instance, elem, validated_data.get(elem))

        instance.save()

        if gallery:
            old_image = instance.gallery.photo_set.all()
            for elem in old_image:
                elem.delete()

            for elem in gallery:
                photo = Photo.objects.create(
                    image=elem.get('image'),
                    gallery=instance.gallery
                )
                photo.save()

        return instance

    def to_representation(self, instance: Complex):
        data = super().to_representation(instance=instance)
        data.update(
            {
                'photo_gallery': PhotoSerializer(instance=instance.gallery.photo_set.all(), many=True).data,
            }
        )
        return data














