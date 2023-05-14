from rest_framework import serializers

from announcements.models import Announcement, Favorites
from residential.models import Complex, Flat
from residential.serializers import ResidentialListSerializer, FlatsInChessBoardApiSerializer


class AnnouncementApiSerializer(serializers.ModelSerializer):
    flat = FlatsInChessBoardApiSerializer(read_only=True)

    class Meta:
        model = Announcement
        fields = ['confirm', 'flat']


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
