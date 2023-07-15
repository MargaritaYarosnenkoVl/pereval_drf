from rest_framework import serializers


from hiker.models import Hiker
from hiker.serializers import HikerSerializer
from .models import Coords, Level, Pereval, Images


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ('latitude', 'longitude', 'height')
        verbose_name = 'Координаты'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ('winter', 'summer', 'autumn', 'spring')
        verbose_name = 'Уровень сложности'


class ImagesSerializer(serializers.ModelSerializer):
    data = serializers.URLField()

    class Meta:
        model = Images
        fields = ('data', 'title')
        verbose_name = 'Фото'


"""Общий сериалайзер для вывода пользователю"""
class PerevalSerializer(serializers.ModelSerializer):
    user = HikerSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer(allow_null=True)
    images = ImagesSerializer(many=True)

    class Meta:
        model = Pereval
        fields = (
             'id', 'beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'user', 'coords', 'level', 'images')

    """Сохранение данных о перевале, полученных от пользователя"""
    def create(self, validated_data, **kwargs):
        user = validated_data.pop('user')
        coords = validated_data.pop('coords')
        level = validated_data.pop('level')
        images = validated_data.pop('images')

        hiker = Hiker.objects.filter(email=user['email'])
        if hiker.exists():
            hiker_serializer = HikerSerializer(data=user)
            hiker_serializer.is_valid(raise_exception=True)
            user = hiker_serializer.save()
        else:
            user = Hiker.objects.create(**user)

        coords = Coords.objects.create(**coords)
        level = Level.objects.create(**level)
        pereval = Pereval.objects.create(**validated_data, user=user, coords=coords, level=level, status='new')

        for image in images:
            data = image.pop('data')
            title = image.pop('title')
            Images.objects.create(data=data, pereval=pereval, title=title)
        return pereval

