from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from announcements.models import *
from residential.models import Complex, Flat, ChessBoard
from residential.serializers import ResidentialListSerializer, FlatsInChessBoardApiSerializer


class AnnouncementApiSerializer(serializers.ModelSerializer):
    flat = FlatsInChessBoardApiSerializer(read_only=True)

    class Meta:
        model = Announcement
        fields = ['confirm', 'flat', 'id']


class FavoriteAnnouncementApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['flat']

    def to_internal_value(self, data):
        # try:
        return Announcement.objects.get(flat_id=data['flat'])
        # except Announcement.DoesNotExist:
        #     raise ValidationError({'corps': _('Корпус не существует')})
        # except (TypeError, IndexError):
        #     raise ValidationError({'corps': _('Неправильно указан корпус')})


class FavoritesApiSerializer(serializers.ModelSerializer):
    announcement = FavoriteAnnouncementApiSerializer()
    residential = ResidentialListSerializer(read_only=True)

    class Meta:
        model = Favorites
        fields = ['announcement', 'residential']

    def create(self, validated_data):
        flat = Flat.objects.get(id=validated_data['announcement'].flat_id)
        favorite = Favorites.objects.create(
            user=self.context.get('user'),
            residential_complex=Complex.objects.get(id=flat.residential_complex.id),
            **validated_data
        )
        return favorite


class PromotionApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'


class AddRequestAnnouncement(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementRequest
        fields = ['announcement']


    def create(self, validated_data):

        announcement = validated_data['announcement']

        try:
            chessboard = ChessBoard.objects.get(corps=announcement.flat.corps, residential_complex=announcement.flat.residential_complex, section=announcement.flat.section)
        except:
            chessboard = ChessBoard.objects.create(corps=announcement.flat.corps, residential_complex=announcement.flat.residential_complex, section=announcement.flat.section)

        try:
            if not AnnouncementRequest.objects.get(announcement=announcement):
                announcement_request = AnnouncementRequest.objects.create(
                    announcement=announcement,
                    chessboard=chessboard
                )
                announcement_request.save()
            else:
                raise ValidationError({'data': _('Запрос уже отправлен')})
        except:
            announcement_request = AnnouncementRequest.objects.create(
                announcement=announcement,
                chessboard=chessboard
            )
            announcement_request.save()
        # except (TypeError, IndexError):
        #     raise ValidationError({'data': _('Такого обьявления не существует')})

        return announcement_request


class RequestAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementRequest
        fields = '__all__'


# class ApproveRequestAnnouncementSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = AnnouncementRequest
#         fields = '__all__'
#
#     def update(self, instance: AnnouncementRequest, validated_data):
#         print(5555555555555555)
#         chess_board = instance.chessboard
#         chess_board.flat.add(instance.announcement.flat)
#         chess_board.save()
#         instance.approve = True
#         instance.save()
#         return instance
