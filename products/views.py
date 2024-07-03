from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.db import transaction
# F - обращение к полям модели и их значениям
from django.db.models import F
from rest_framework.response import Response

from products.models import *
from products.serializers import *
from django.shortcuts import render

from products.filters import ProductListFilter
from django_filters.rest_framework import DjangoFilterBackend


# Возвращает список главных категорий (страница Меню). Фильтруем таблицу по parent_id
class MainCategoryListAPIView(ListAPIView):
    queryset = CategoryList.objects.filter(parent_id=1).order_by('order')
    serializer_class = ProductCategoryListSerializer
    pagination_class = None


# подробные данные для страницы с продуктом
class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


# список продуктов
class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductDetailSerializer
    filter_backends = [DjangoFilterBackend]

# список продуктов с фильтрацией
class ProductFilterListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    filter_backends = [DjangoFilterBackend]
    ordering_filter = ['price']
    filterset_class = ProductListFilter

class CreateOrderAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer

    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                # items - ключ продуктов, которые приходят внутри запроса
                items = self.request.data.pop('products')
                order = Order.objects.create(**self.request.data)
                total_price = 0

                for item in items:
                    try:
                        # OrderItem - модель, товары в составе заказа
                        new_order_item = OrderItem.objects.create(order=order,
                                                                  **item)
                        total_price += new_order_item.total_price
                    except OrderItem.DoesNotExist:
                        return Response(data={'error': 'Cart item does not exist.'}, status=400)

                Order.objects.filter(id=order.id).update(total_price=F('total_price') + total_price)
                return Response(data={'order_id': order.id})
        except Exception as e:
            return Response(data={'error': str(e)}, status=500)



