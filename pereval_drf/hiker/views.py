from .serializers import *
from rest_framework import viewsets


class PassUserViewSet(viewsets.ModelViewSet):
    queryset = Hiker.objects.all()
    serializer_class = HikerSerializer
