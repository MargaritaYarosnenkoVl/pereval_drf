from django.http import JsonResponse
from rest_framework import  status, mixins, generics
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Pereval
from .serializers import PerevalSerializer


class PerevalViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     GenericViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer

    """Создание объекта перевала"""
    def create(self, request, *args, **kwargs):
        serializer = PerevalSerializer(data=request.data)

        """Результаты метода: JSON"""
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'message': None,
                'id': serializer.data['id'],
            })
        if status.HTTP_400_BAD_REQUEST:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Bad Request',
                'id': None,
            })
        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Ошибка подключения к базе данных',
                'id': None,
            })

    """Изменение объекта перевала id (кроме полей с данными пользователя)"""
    def partial_update(self, request, *args, **kwargs):
        pereval = self.get_object()
        if pereval.status == 'new':
            serializer = PerevalSerializer(pereval, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'state': '1',
                    'message': 'Запись успешно изменена'
                })
            else:
                return Response({
                    'state': '0',
                    'message': serializer.errors
                })
        else:
            return Response({
                'state': '0',
                'message': f"Не удалось обновить запись: {pereval.get_status_display()}"
            })


"""GET запрос для вывода всех записей по email пользователя"""
class EmailAPIView(generics.ListAPIView):
    serializer_class = PerevalSerializer

    def get(self, request, *args, **kwargs):
        email = kwargs.get('email', None)
        if Pereval.objects.filter(user__email=email):
            data = PerevalSerializer(Pereval.objects.filter(user__email=email), many=True).data
        else:
            data = {
                'message': f'Not exist email hjh{email}'
            }
        return JsonResponse(data, safe=False)



