from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.relations import PrimaryKeyRelatedField

from announcements.models import Announcement
from files.models import Gallery, Photo
from files.serializers import PhotoSerializer
from residential.models import *
from users.serializers import AuthUserSerializer
from django.utils.translation import gettext_lazy as _


class ResidentialListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Complex
        fields = ['id', 'name']

    def to_internal_value(self, data: int) -> Complex:
        try:
            return Complex.objects.get(id=data['name'])
        except:
            raise ValidationError({'detail': _('ЖК не существует')})


class UploadedBase64ImageSerializer(serializers.Serializer):
    photo = Base64ImageField(required=False)


class Residential64Serializer(serializers.ModelSerializer):
    photo = Base64ImageField()
    photo_gallery = PhotoSerializer(many=True, required=False)
    user = AuthUserSerializer(read_only=True)

    class Meta:
        model = Complex
        exclude = ['gallery']

    def create(self, validated_data):
        gallery = validated_data.pop('photo_gallery', None)
        if not Complex.objects.filter(user=self.context['request'].user):
            res_complex = Complex.objects.create(
                user=self.context['request'].user,
                gallery=Gallery.objects.create(name='residential_complex'),
                **validated_data
            )
        else:
            raise ValidationError(detail={'data': _('user have residential_complex')}, code=status.HTTP_400_BAD_REQUEST)

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

class ResidentialSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField()
    photo_gallery = PhotoSerializer(many=True, required=False)
    user = AuthUserSerializer(read_only=True)

    class Meta:
        model = Complex
        exclude = ['gallery']

    def create(self, validated_data):
        gallery = validated_data.pop('photo_gallery', None)
        if not Complex.objects.filter(user=self.context['request'].user):
            res_complex = Complex.objects.create(
                user=self.context['request'].user,
                gallery=Gallery.objects.create(name='residential_complex'),
                **validated_data
            )
        else:
            raise ValidationError(detail={'data': _('user have residential_complex')}, code=status.HTTP_400_BAD_REQUEST)

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

        try:
            if gallery:
                old_image = Photo.objects.filter(gallery=instance.gallery)
                for elem in old_image:
                    elem.delete()

                for elem in gallery:
                    photo = Photo.objects.create(
                        image=elem.get('image'),
                        gallery=instance.gallery
                    )
                    photo.save()
        except:
            return instance

        return instance

    def to_representation(self, instance: Complex):
        data = super().to_representation(instance=instance)
        data.update(
            {
                'photo_gallery': PhotoSerializer(instance=instance.gallery.photo_set.all(), many=True).data,
            }
        )
        return data


class SectionApiSerializer(serializers.ModelSerializer):
    residential_complex = PrimaryKeyRelatedField(queryset=Complex.objects.all(), required=False)

    class Meta:
        model = Section
        fields = '__all__'


class CorpsApiSerializer(serializers.ModelSerializer):
    residential_complex = PrimaryKeyRelatedField(queryset=Complex.objects.all(), required=False)

    class Meta:
        model = Corps
        fields = '__all__'


class FloorApiSerializer(serializers.ModelSerializer):
    residential_complex = PrimaryKeyRelatedField(queryset=Complex.objects.all(), required=False)

    class Meta:
        model = Floor
        fields = '__all__'


class DocumentApiSerializer(serializers.ModelSerializer):
    residential_complex = PrimaryKeyRelatedField(queryset=Complex.objects.all(), required=False)

    class Meta:
        model = Documents
        fields = '__all__'


class NewsApiSerializer(serializers.ModelSerializer):
    residential_complex = PrimaryKeyRelatedField(queryset=Complex.objects.all(), required=False)

    class Meta:
        model = News
        fields = '__all__'


class SectionFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'name']

    def to_internal_value(self, data: int):
        try:
            return Section.objects.select_related('residential_complex').get(pk=data['name'])
        except Section.DoesNotExist:
            raise ValidationError({'section': _('Секция не существует')})
        except (TypeError, IndexError):
            raise ValidationError({'section': _('Неправильно указана секция')})


class CorpsFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corps
        fields = ['id', 'name']

    def to_internal_value(self, data: int):
        try:
            return Corps.objects.select_related('residential_complex').get(pk=data['name'])
        except Corps.DoesNotExist:
            raise ValidationError({'corps': _('Корпус не существует')})
        except (TypeError, IndexError):
            raise ValidationError({'corps': _('Неправильно указан корпус')})


class FloorFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ['id', 'name']

    def to_internal_value(self, data: int):
        try:
            return Floor.objects.select_related('residential_complex').get(pk=data['name'])
        except Floor.DoesNotExist:
            raise ValidationError({'floor': _('Этажа не существует')})
        except (TypeError, IndexError):
            raise ValidationError({'floor': _('Неправильно указан этаж')})


class FlatApiSerializer(serializers.ModelSerializer):
    residential_complex = ResidentialListSerializer()
    section = SectionFlatSerializer()
    floor = FloorFlatSerializer()
    corps = CorpsFlatSerializer()
    scheme = Base64ImageField(use_url=True)
    photo_gallery = PhotoSerializer(many=True, required=False)
    user = AuthUserSerializer(read_only=True)

    class Meta:
        model = Flat
        exclude = ['gallery']


    def validate(self, attrs):
        if attrs.get('section', None) and attrs.get('floor', None) and attrs.get('corps', None):
            if attrs.get('section', None).residential_complex != attrs.get('floor').residential_complex != attrs.get('corps').residential_complex != self.context.get('residential_complex', None):
                raise ValidationError({'corps': _('Корпус, секция и этаж должны быть с одного ЖК'),
                                       'section': _('Корпус, секция и этаж должны быть с одного ЖК'),
                                       'floor': _('Корпус, секция и этаж должны быть с одного ЖК')})
        return super().validate(attrs)

    def create(self, validated_data):
        gallery = validated_data.pop('photo_gallery', None)
        flat = Flat.objects.create(
            user=self.context['request'].user,
            gallery=Gallery.objects.create(name='flat'),
            **validated_data

        )
        announcement = Announcement.objects.create(confirm=True, flat=flat)
        announcement.save()
        # try:
        #     chess_board = ChessBoard.objects.get(residential_complex=self.context.get('residential_complex'),
        #                             section=validated_data['section'], corps=validated_data['corps'])
        # except:
        #     chess_board = False
        #
        # if chess_board:
        #     chess_board.flat.add(flat)
        #     chess_board.save()
        if gallery:
            for elem in gallery:
                photo = Photo.objects.create(
                    image=elem.get('image'),
                    gallery=flat.gallery
                )
                photo.save()
        return flat

    def update(self, instance: Flat, validated_data):
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


class FlatsInChessBoardApiSerializer(serializers.ModelSerializer):
    floor = FloorFlatSerializer()

    class Meta:
        model = Flat
        fields = ['id', 'floor', 'scheme', 'price', 'square']


class ChessBoardApiSerializer(serializers.ModelSerializer):
    residential_complex = ResidentialListSerializer(read_only=True)
    section = SectionFlatSerializer()
    corps = CorpsFlatSerializer()
    flats = FlatsInChessBoardApiSerializer(source='flat', read_only=True, many=True)

    class Meta:
        model = ChessBoard
        fields = ['residential_complex', 'section', 'corps', 'flats']

    def validate(self, attrs):
        if attrs.get('section', None) and attrs.get('corps', None):
            if attrs.get('section', None).residential_complex != attrs.get('corps').residential_complex != self.context.get('residential_complex', None):
                raise ValidationError({'corps': _('Корпус, секция и этаж должны быть с одного ЖК'),
                                       'section': _('Корпус, секция и этаж должны быть с одного ЖК')})
        return super().validate(attrs)

    def create(self, validated_data):
        flat = validated_data.pop('flats', None)
        validated_data['residential_complex'] = self.context.get('residential_complex')
        chess_board = ChessBoard.objects.create(**validated_data)
        # flats = Flat.objects.filter(residential_complex=self.context.get('residential_complex'), section=validated_data['section'], corps=validated_data['corps'])
        # if flats:
        #     for flat in flats:
        #         chess_board.flat.add(flat)
        chess_board.save()
        return chess_board












