from rest_framework import serializers

from products.models import *
from common.serializers import MediaURLSerializer

# Сериалайзер, который собирает картинки для продукта
class ProductImageSerializer(serializers.ModelSerializer):
    image = MediaURLSerializer()

    class Meta:
        model = ProductImage
        exclude = ["product"]
        read_only_fields = ['id', 'image']

# сериалайзер списка продуктов c категориями
class ProductCategorySerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.title')
    category = serializers.CharField(source='category.title')

    class Meta:
        model = ProductCategory
        fields = ('id', 'product', 'category')
        # поля должны быть только для чтения
        read_only_fields = fields

# сериалайзер списка тэгов
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title')
        # поля должны быть только для чтения
        read_only_fields = fields

# сериалайзер списка тэгов для продукта. От ДЕТЕЙ к РОДИТЕЛЯМ
class ProductTagSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()
    class Meta:
        model = ProductTag
        fields = ('item', )
        read_only_fields = fields

    def get_item(self, obj):
        return TagSerializer(obj.tag).data

# сериалайзер списка Причин
class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ('id', 'title')
        # поля должны быть только для чтения
        read_only_fields = fields

# сериалайзер списка причин для продукта. От ДЕТЕЙ к РОДИТЕЛЯМ
class ProductReasonSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()
    class Meta:
        model = ProductReason
        fields = ('item', )
        read_only_fields = fields

    def get_item(self, obj):
        return ReasonSerializer(obj.reason).data

# Сериалайзер для продукта (не от МОДЕЛИ)
class ProductDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    category = serializers.CharField(source='category.title')
    desc = serializers.CharField()
    price = serializers.FloatField()
    discount = serializers.FloatField()
    final_price = serializers.SerializerMethodField()
    image = MediaURLSerializer()
    # ссылка на сериалайзер, который собирает картинки для продукта
    product_images = ProductImageSerializer(many=True)
    # ссылка на сериалайзер, который собирает tags
    product_tag = ProductTagSerializer(many=True)
    # ссылка на сериалайзер, который собирает reason
    product_reason = ProductReasonSerializer(many=True)

    def get_final_price(self, obj):
        return obj.price * (100 - obj.discount)/100

# сериалайзер списка категорий
class ProductCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryList
        fields = ('id', 'title', 'image')


# продукты для заказа
class OrderItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

# создание заказа
class CreateOrderSerializer(serializers.ModelSerializer):
    # нужно обратиться от Родителя к Детям - от Order к OrderItem
    # без related_name ссылка на "детей" - child=OrderItemSerializer()
    products = serializers.ListSerializer(child=OrderItemSerializer())

    class Meta:
        model = Order
        fields = ('full_name', 'phone_number', 'products')

# ------------------------------------------------------------------

class ProductDetailSerializer1(serializers.ModelSerializer):
    image = MediaURLSerializer()  # python objects - url image
    # вытащит все images:
    product_images = ProductImageSerializer(many=True)
    # Показать все tags:
    product_tag = ProductTagSerializer(many=True)

    class Meta:
        model = Product
        # поля из модели:
        fields = ('id', 'title', 'desc', 'price', 'category', 'image',
                  # поля, которые мы объявили, определяя детей сервисов:
                  'product_images', 'product_tag')
