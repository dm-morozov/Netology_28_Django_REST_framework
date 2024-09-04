from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Weapon
from .serializers import WeaponSerializerTwo

# @api_view(['GET', 'POST'])
# def demo(request):
#     if request.method == 'GET':
#         weapon = Weapon.objects.all()

#         # Используем сериализатор для преобразования QuerySet в JSON-совместимый формат
#         serializer = WeaponSerializerTwo(weapon, many=True)

#         data = {
#             'message': 'Hello',
#             'weapon': serializer.data, # Используем сериализованные данные
#         }
#         return Response(serializer.data)

#     if request.method == 'POST':
#         ok = {'status': 'ok'}
#         return Response(ok)


class DemoView(APIView):

    def get(self, request, *args, **kwargs):
        """
        Обработка GET-запросов для получения всех объектов Weapon.
        """
        weapon = Weapon.objects.all()

        # Используем сериализатор для преобразования QuerySet в JSON-совместимый формат
        serializer = WeaponSerializerTwo(weapon, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Обработка POST-запросов для создания нового объекта Weapon.
        """
        serializer = WeaponSerializerTwo(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DemoViewTwo(ListAPIView):
    queryset = Weapon.objects.all()
    serializer_class = WeaponSerializerTwo

    def post(self, request, *args, **kwargs):
        """
        Обработка POST-запросов для создания нового объекта Weapon.
        """
        serializer = WeaponSerializerTwo(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Обработка DELETE-запросов для удаления объекта Weapon.
        """
        # Извлекаем идентификатор объекта из URL
        weapon_id = kwargs.get('id', None)  # предполагается, что 'id' передается в URL

        # Проверяем, был ли передан ID
        if weapon_id is None:
            return Response({"error": "ID не предоставлен"}, status=status.HTTP_400_BAD_REQUEST)

        # Попытка получить объект Weapon по ID, если не найден, возвращает 404 ошибку
        weapon = get_object_or_404(Weapon, id=weapon_id)

        # Удаляем объект
        weapon.delete()

        # Возвращаем успешный ответ
        return Response({"message": "Weapon успешно удален"}, status=status.HTTP_204_NO_CONTENT)
    

class WeaponView(RetrieveAPIView):
    queryset = Weapon.objects.all()
    serializer_class = WeaponSerializerTwo
        