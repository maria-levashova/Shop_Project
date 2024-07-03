from rest_framework.generics import RetrieveAPIView

from common.serializers import *
from common.models import *


class ConfigView(RetrieveAPIView):
    # какой сериалайзер будет использован:
    serializer_class = ConfigSerializer
    # queryset - запросы в БД. Settings – имя собственное МОДЕЛИ
    queryset = Settings.objects.all()

    # из всех (objects.all()) выбрать ОДИН объект, т.к. класс возвращает один объект
    def get_object(self):
        return Settings.objects.first()

