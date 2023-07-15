from rest_framework import serializers
from .models import Hiker


class HikerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hiker
        fields = ('email', 'fam', 'name', 'otc', 'phone',)
        verbose_name = 'Турист'

    """Сохранение пользователя"""
    def save(self, **kwargs):
        self.is_valid()
        hiker = Hiker.objects.filter(email=self.validated_data.get('email'))
        if hiker.exists():
            return hiker.first()
        else:
            return Hiker.objects.create(
                email=self.validated_data.get('email'),
                fam=self.validated_data.get('fam'),
                name=self.validated_data.get('name'),
                otc=self.validated_data.get('otc'),
                phone=self.validated_data.get('phone'),
            )

