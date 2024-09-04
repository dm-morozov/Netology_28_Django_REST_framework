# Учебный проект: Django REST Framework (DRF)

## Описание проекта

Этот учебный проект посвящен изучению Django REST Framework (DRF) — мощного инструмента для создания RESTful API на базе Django. В процессе работы над проектом мы освоили основные принципы и подходы к созданию API, включая сериализацию данных, обработку запросов и реализацию представлений.

## Основные цели

1. **Изучить основные концепции Django REST Framework:**
    - Сериализация данных с использованием классов `Serializer` и `ModelSerializer`.
    - Реализация обработчиков запросов с использованием функций (FBV) и классов (CBV).
    - Создание и управление API-эндпоинтами для работы с данными.
2. **Практическое применение полученных знаний:**
    - Создание моделей и сериализаторов для обработки данных.
    - Настройка маршрутов для обработки различных HTTP-запросов.
    - Работа с различными типами представлений в DRF.

## Структура проекта

### 1. **Модель `Weapon`**

В проекте реализована модель `Weapon`, которая представляет собой объект оружия с полями:

- `power`: Мощность оружия (целое число).
- `rarity`: Редкость оружия (строка).
- `value`: Ценность оружия (целое число).

```python
from django.db import models

class Weapon(models.Model):
    power = models.IntegerField()
    rarity = models.CharField(max_length=50)
    value = models.IntegerField()
```

### 2. **Сериализаторы**

В проекте созданы два вида сериализаторов для модели `Weapon`:

- **`WeaponSerializerOne`**: Использует класс `Serializer` и явно определяет поля для сериализации.
- **`WeaponSerializerTwo`**: Использует класс `ModelSerializer`, который автоматически генерирует поля на основе модели.

```python
from rest_framework import serializers
from .models import Weapon

class WeaponSerializerOne(serializers.Serializer):
    power = serializers.IntegerField()
    rarity = serializers.CharField()

class WeaponSerializerTwo(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        fields = ['id', 'power', 'rarity', 'value']
```

### 3. **Представления**

Проект включает несколько видов представлений для обработки запросов:

- **`DemoView`** (на основе класса `APIView`):
    - Обрабатывает GET-запросы для получения всех объектов модели `Weapon`.
    - Обрабатывает POST-запросы для создания нового объекта `Weapon`.

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Weapon
from .serializers import WeaponSerializerTwo

class DemoView(APIView):

    def get(self, request, *args, **kwargs):
        weapon = Weapon.objects.all()
        serializer = WeaponSerializerTwo(weapon, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = WeaponSerializerTwo(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

- **`DemoViewTwo`** (на основе класса `ListAPIView`):
    - Обрабатывает GET-запросы для получения списка объектов `Weapon`.
    - Поддерживает создание новых объектов через POST-запросы и удаление существующих через DELETE-запросы.

```python
from rest_framework.generics import ListAPIView, get_object_or_404

class DemoViewTwo(ListAPIView):
    queryset = Weapon.objects.all()
    serializer_class = WeaponSerializerTwo

    def post(self, request, *args, **kwargs):
        serializer = WeaponSerializerTwo(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        weapon_id = kwargs.get('id', None)
        if weapon_id is None:
            return Response({"error": "ID не предоставлен"}, status=status.HTTP_400_BAD_REQUEST)

        weapon = get_object_or_404(Weapon, id=weapon_id)
        weapon.delete()
        return Response({"message": "Weapon успешно удален"}, status=status.HTTP_204_NO_CONTENT)
```

- **`WeaponView`** (на основе класса `RetrieveAPIView`):
    - Обрабатывает GET-запросы для получения одного объекта `Weapon` по его первичному ключу (ID).

```python
from rest_framework.generics import RetrieveAPIView

class WeaponView(RetrieveAPIView):
    queryset = Weapon.objects.all()
    serializer_class = WeaponSerializerTwo
```

### 4. **Маршрутизация**

В проекте настроены URL-маршруты для обработки запросов:

```python
from django.urls import path
from .views import DemoView, DemoViewTwo, WeaponView

urlpatterns = [
    path('demo/', DemoView.as_view()),
    path('demotwo/', DemoViewTwo.as_view()),
    path('demotwo/<int:id>/', DemoViewTwo.as_view(), name='demotwo'),
    path('weapon/<int:pk>/', WeaponView.as_view()),
]
```

### 5. **Примеры HTTP-запросов**

- **GET запрос для получения списка объектов `Weapon`:**
    
    ```bash
    GET http://localhost:8000/demo/
    ```
    
- **POST запрос для создания нового объекта `Weapon`:**
    
    ```bash

    POST http://localhost:8000/demo/
    Content-Type: application/json
    
    {
      "power": 50,
      "rarity": "Rare",
      "value": 150
    }
    
    ```
    
- **GET запрос для получения одного объекта `Weapon` по ID:**
    
    ```bash
    GET http://localhost:8000/weapon/1/
    ```
    
- **DELETE запрос для удаления объекта `Weapon`:**
    
    ```bash
    DELETE http://localhost:8000/demotwo/3/
    ```
    

## Чему мы научились

1. **Сериализация данных:**
    - Создание сериализаторов с использованием классов `Serializer` и `ModelSerializer`.
    - Преобразование объектов моделей в JSON и обратно.
    - Работа с вложенными сериализаторами и сложными отношениями между моделями.
2. **Работа с представлениями:**
    - Реализация функциональных представлений (FBV) с использованием декоратора `@api_view`.
    - Создание классов представлений (CBV) на основе `APIView`, `ListAPIView`, и `RetrieveAPIView`.
    - Обработка различных HTTP-запросов (GET, POST, DELETE) и возвращение соответствующих ответов.
3. **Маршрутизация и организация API:**
    - Настройка URL-маршрутов для взаимодействия с API.
    - Управление ресурсами через эндпоинты, поддерживающие CRUD-операции.

## Заключение

Этот проект дал нам ценные знания и опыт работы с Django REST Framework, который является стандартом де-факто для создания API на базе Django. Мы рассмотрели ключевые аспекты создания API, такие как сериализация данных, работа с представлениями и обработка запросов. Эти навыки обеспечат уверенность при разработке и поддержке RESTful API в реальных проектах.