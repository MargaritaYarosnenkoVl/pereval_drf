import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from hiker.models import Hiker

from .models import Pereval, Coords, Level, Images
from .serializers import PerevalSerializer


"""Тест, проверяющий создание новых перевалов"""
class PerevalAddTests(APITestCase):
    def setUp(self) -> None:
        self.pereval_1 = Pereval.objects.create(
            user=Hiker.objects.create(
                email="Test1@mail.ru",
                fam="Test1",
                name="Test1",
                otc="Test1",
                phone="1"
            ),
            beauty_title="Test1",
            title="Test1",
            other_titles="Test1",
            connect='',
            coords=Coords.objects.create(
                latitude=1,
                longitude=1,
                height=1
            ),
            level=Level.objects.create(
                winter='А1',
                summer='',
                autumn='А1',
                spring='А1'
            )
        )
        self.image_1 = Images.objects.create(
            data="https://online-pereval.ru/1.jpg",
            title="Test1",
            pereval=self.pereval_1
        )
        self.image_2 = Images.objects.create(
            data="https://online-pereval.ru/2.jpg",
            title="Test1",
            pereval=self.pereval_1
        )

        self.pereval_2 = Pereval.objects.create(
            user=Hiker.objects.create(
                email="Test2@mail.ru",
                fam="Test2",
                name="Test2",
                otc="Test2",
                phone="2"
            ),
            beauty_title="Test2",
            title="Test2",
            other_titles="Test2",
            connect='',
            coords=Coords.objects.create(
                latitude=2,
                longitude=2,
                height=2),
            level=Level.objects.create(
                winter='',
                summer='',
                autumn='',
                spring=''
            )
        )
        self.image_1 = Images.objects.create(
            data="https://online-pereval.ru/1.jpg",
            title="Test2",
            pereval=self.pereval_2
        )
        self.image_2 = Images.objects.create(
            data="https://online-pereval.ru/2.jpg",
            title="Test2",
            pereval=self.pereval_2
        )

        self.pereval_3 = Pereval.objects.create(
            user=Hiker.objects.create(
                email="Test3@mail.ru",
                fam="Test3",
                name="Test3",
                otc="Test3",
                phone="3"
            ),
            beauty_title="Test3",
            title="Test3",
            other_titles="Test3",
            connect='',
            coords=Coords.objects.create(
                latitude=3,
                longitude=3,
                height=3),
            level=Level.objects.create(
                winter='',
                summer='',
                autumn='',
                spring=''
            ),
            status='pending'
        )
        self.image_1 = Images.objects.create(
            data="https://online-pereval.ru/1.jpg",
            title="Test3",
            pereval=self.pereval_3
        )
        self.image_2 = Images.objects.create(
            data="https://online-pereval.ru/1.jpg",
            title="Test3",
            pereval=self.pereval_3
        )

    def test_get_list(self):
        url = reverse('pereval-list')
        response = self.client.get(url)
        serializer_data = PerevalSerializer([self.pereval_1, self.pereval_2, self.pereval_3], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(len(serializer_data), 3)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.json())

    def test_get_detail(self):
        url = reverse('pereval-detail', args=(self.pereval_1.id,))
        response = self.client.get(url)
        serializer_data = PerevalSerializer(self.pereval_1).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.json())


class PerevalSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.pereval_1 = Pereval.objects.create(
            user=Hiker.objects.create(
                email="Test1@mail.ru",
                fam="Test1",
                name="Test1",
                otc="Test1",
                phone="1"
            ),
            beauty_title="Test1",
            title="Test1",
            other_titles="Test1",
            connect='',
            coords=Coords.objects.create(
                latitude=1,
                longitude=1,
                height=1
            ),
            level=Level.objects.create(
                winter='',
                summer='',
                autumn='',
                spring=''
            )
        )
        self.image_1 = Images.objects.create(
            data="https://online-pereval.ru/1.jpg",
            title="Test1",
            pereval=self.pereval_1
        )
        self.image_2 = Images.objects.create(
            data="https://online-pereval.ru/2.jpg",
            title="Test1",
            pereval=self.pereval_1
        )

        self.pereval_2 = Pereval.objects.create(
            user=Hiker.objects.create(
                email="Test2@mail.ru",
                fam="Test2",
                name="Test2",
                otc="Test2",
                phone="2"
            ),
            beauty_title="Test2",
            title="Test2",
            other_titles="Test2",
            connect='',
            coords=Coords.objects.create(
                latitude=2,
                longitude=2,
                height=2),
            level=Level.objects.create(
                winter='',
                summer='',
                autumn='',
                spring=''
            )
        )
        self.image_1 = Images.objects.create(
            data="https://online-pereval.ru/1.jpg",
            title="Test2",
            pereval=self.pereval_2
        )
        self.image_2_2 = Images.objects.create(
            data="https://online-pereval.ru/2.jpg",
            title="Test2",
            pereval=self.pereval_2
        )

    def test_check(self):
        serializer_data = PerevalSerializer([self.pereval_1, self.pereval_2], many=True).data
        expected_data = [
            {
                'id': self.pereval_1.id,
                'user': {
                    'email': 'Test1@mail.ru',
                    'name': 'Test1',
                    'fam': 'Test1',
                    'otc': 'Test1',
                    'phone': '1'
                },
                'beauty_title': 'Test1',
                'title': 'Test1',
                'other_titles': 'Test1',
                'connect': '',
                'coords': {
                    'latitude': 1,
                    'longitude': 1,
                    'height': 1
                },
                'level': {
                    'winter': '',
                    'summer': '',
                    'autumn': '',
                    'spring': ''
                },
                'images': [
                    {
                        'data': 'https://online-pereval.ru/1.jpg',
                        'title': 'Test1'
                    },
                    {
                        'data': 'https://online-pereval.ru/2.jpg',
                        'title': 'Test1'
                    }
                ],
                'status': 'new'
            },
            {
                'id': self.pereval_2.id,
                'user': {
                    'email': 'Test2@mail.ru',
                    'name': 'Test2',
                    'fam': 'Test2',
                    'otc': 'Test2',
                    'phone': '2'
                },
                'beauty_title': 'Test2',
                'title': 'Test2',
                'other_titles': 'Test2',
                'connect': '',
                'coords': {
                    'latitude': 2,
                    'longitude': 2,
                    'height': 2
                },
                'level': {
                    'winter': '',
                    'summer': '',
                    'autumn': '',
                    'spring': ''
                },
                'images': [
                    {
                        'data': 'https://online-pereval.ru/1.jpg',
                        'title': 'Test2'
                    },
                    {
                        'data': 'https://online-pereval.ru/2.jpg',
                        'title': 'Test2'
                    }
                ],
                'status': 'new'
            }
        ]
        self.assertEqual(expected_data, serializer_data)
