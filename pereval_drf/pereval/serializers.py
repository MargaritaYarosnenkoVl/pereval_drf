from rest_framework import serializers


from hiker.models import Hiker
from hiker.serializers import HikerSerializer
from .models import Coords, Level, Pereval, Images
from drf_writable_nested import WritableNestedModelSerializer

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
class PerevalSerializer(WritableNestedModelSerializer):
    user = HikerSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer(allow_null=True)
    images = ImagesSerializer(many=True)

    class Meta:
        model = Pereval
        fields = (
             'id', 'beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'user', 'coords', 'level', 'images', 'status')

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

    """Сохранение данных о перевале, измененных пользователем"""
    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user
            data_user = data.get('user')
            validating_user_fields = [
                instance_user.fam != data_user['fam'],
                instance_user.name != data_user['name'],
                instance_user.otc != data_user['otc'],
                instance_user.phone != data_user['phone'],
                instance_user.email != data_user['email'],
            ]
            if data_user is not None and any(validating_user_fields):
                raise serializers.ValidationError({'Не удалось обновить запись': 'Нельзя изменять данные пользователя'})
        return data

