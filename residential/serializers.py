from rest_framework import serializers

from residential.models import Complex


class ResidentialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Complex
        fields = '__all__'