from django.db import models
from pereval.utils import get_path_upload_photos
from hiker.models import Hiker


class Pereval(models.Model):
    NEW = 'new'
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    STATUS_CHOICES = [
    ("new", "новый"),
    ("pending",  "модератор взял в работу"),
    ("accepted", "модерация прошла успешно"),
    ("rejected",  "модерация прошла, информация не принята"),
    ]

    beauty_title = models.CharField(max_length=255, verbose_name='Название препятствия', null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name='Название вершины', null=True, blank=True)
    other_titles = models.CharField(max_length=255, verbose_name='Другое название', null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Hiker, on_delete=models.CASCADE, related_name='user')
    coords = models.ForeignKey('Coords', on_delete=models.CASCADE, null=True, blank=True)
    level = models.ForeignKey('Level', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=NEW)
    connect = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.pk}: {self.beauty_title}"

    class Meta:
        verbose_name = "Перевал"
        verbose_name_plural = "Перевалы"


class Coords(models.Model):
    latitude = models.FloatField(max_length=50, verbose_name='Широта', null=True, blank=True)
    longitude = models.FloatField(max_length=50, verbose_name='Долгота', null=True, blank=True)
    height = models.IntegerField(verbose_name='Высота', null=True, blank=True)

    def __str__(self):
        return f"широта: {self.latitude}, долгота: {self.longitude}, высота: {self.height}"

    class Meta:
        verbose_name = "Координаты"
        verbose_name_plural = "Координаты"


class Level(models.Model):
    winter = models.CharField(max_length=10, verbose_name='Зима', null=True, blank=True)
    summer = models.CharField(max_length=10, verbose_name='Лето', null=True, blank=True)
    autumn = models.CharField(max_length=10, verbose_name='Осень', null=True, blank=True)
    spring = models.CharField(max_length=10, verbose_name='Весна', null=True, blank=True)

    def __str__(self):
        return f"зима: {self.winter}, весна: {self.spring}, лето: {self.summer}, осень: {self.autumn}"

    class Meta:
        verbose_name = "Уровень сложности"
        verbose_name_plural = "Уровни сложности"


class Images(models.Model):
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    data = models.ImageField(upload_to=get_path_upload_photos, verbose_name='Изображение', null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk}: {self.title}"

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"


