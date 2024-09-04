from rest_framework import serializers

from .models import Weapon


class WeaponSerializerOne(serializers.Serializer):
    power = serializers.IntegerField()
    rarity = serializers.CharField()


class WeaponSerializerTwo(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        # fields = '__all__'
        fields = ['id', 'power', 'rarity', 'value']