import datetime
# MPTTModel - поддержка древовидной структуры
from mptt.models import MPTTModel, TreeForeignKey

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from common.utils import validate_phone_number

# CategoryList - модель для списка категорий
class CategoryList(MPTTModel):
    title = models.CharField(max_length=100,
                             verbose_name=_("Title"),
                             unique=True)
    order = models.IntegerField(_("Order"), default=0)

    # image - поле для главной картинки Сервиса
    image = models.ForeignKey('common.Media',
                              on_delete=models.CASCADE,
                              verbose_name=_("Image"),
                              blank=True, null=True)

    # ссылка на родительскую категорию. self дает возможность ссылаться на экземпляр той же модели
    # обратиться от детей к родителям: имя_ребенка.parent.title, где parent - поле модели (таблицы БД)
    # От родителей к детям - нужен related_name = "children"

    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            null=True, blank=True,
                            related_name="children")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Category List")
        verbose_name_plural = _("Category Lists")
        ordering = ['order']

    # для автоматического заполнения title будет автоматически подставлять order
    class MPTTMeta:
        order_insertion_by = ['title']

# Product - модель для продуктов
class Product(models.Model):
    category = models.ForeignKey(CategoryList,
                                 on_delete=models.CASCADE,
                                 verbose_name=_("Category Title"),
                                 related_name="products")
    title = models.CharField(_("Title"), max_length=100)

    # image - поле для главной картинки Сервиса
    image = models.ForeignKey('common.Media',
                              on_delete=models.CASCADE,
                              verbose_name=_("Image"))

    desc = models.TextField(_("Description"))
    price = models.IntegerField(_("price"))
    discount = models.DecimalField(decimal_places=2, max_digits=5, verbose_name=_("discount"))
    created_at = models.DateField(_("created_at"))
    is_in_stock = models.BooleanField(_("is in stock"),
                                       default=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Product")

    def __str__(self):
        return self.title

# ProductImage - подмодель главной родительской модели Product
class ProductImage(models.Model):
    image = models.ForeignKey('common.Media', on_delete=models.CASCADE,
                              verbose_name=_("Image"))
    # related_name = 'images' - для обращения к родителям
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name=_("Product"),
                                related_name='product_images')

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self):
        return f"Id: {self.id}| Product: {self.product.title}"

# модель для хранения продукт-категория
class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name=_("Product"),
                                related_name='pcat_product')
    category = models.ForeignKey(CategoryList, on_delete=models.CASCADE,
                              verbose_name=_("Category"),
                              related_name='pcat_category')

    class Meta:
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")

    def __str__(self):
        return f"Id: {self.id}| Product: {self.product.title} | Category: {self.category.title}"

class Tag(models.Model):
    title = models.CharField(max_length=100,
                             verbose_name=_("Title"),
                             unique=True)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return f"{self.id}| {self.title}"

# модель для хранения продукт-тэги
class ProductTag(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name=_("Product"),
                                related_name='product_tag')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE,
                                verbose_name=_("Tag"),
                                related_name='tags_of_products')

    class Meta:
        verbose_name = _("Product Tag")
        verbose_name_plural = _("Product Tags")

    def __str__(self):
        return f"Id: {self.id}| Product: {self.product.title} | Tag: {self.tag.title}"

# поводы
class Reason(models.Model):
    title = models.CharField(max_length=100,
                             verbose_name=_("Title"),
                             unique=True)

    class Meta:
        verbose_name = _("Reason")
        verbose_name_plural = _("Reasons")

    def __str__(self):
        return f"{self.id}| {self.title}"

# модель для хранения продукт-повод
class ProductReason(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name=_("Product"),
                                related_name='product_reason')
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE,
                                verbose_name=_("Reason"),
                                related_name='reasons_of_products')

    class Meta:
        verbose_name = _("Product Reason")
        verbose_name_plural = _("Product Reasons")

    def __str__(self):
        return f"Id: {self.id}| Product: {self.product.title} | Tag: {self.reason.title}"


# Заказы пользователей
# Статус присваивается по дефолту default=OrderStatus.NEW, но может быть изменен админом
class Order(models.Model):
    class OrderStatus(models.TextChoices):
        NEW = 'new', _('new')
        ACCEPTED = 'accepted', _('accepted')
        PROGRESS = 'progress', _('progress')
        CANCELLED = 'cancelled', _('cancelled')
        FINISHED = 'finished', _('finished')

    full_name = models.CharField(_("full name"), max_length=120)
    phone_number = models.CharField(_("phone number"), max_length=20,
                                    validators=[validate_phone_number])
    status = models.CharField(_("status"), max_length=20,
                              choices=OrderStatus.choices,
                              default=OrderStatus.NEW)
    total_price = models.FloatField(_("total price"), default=0)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self):
        return self.full_name

# товары в составе заказа
class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name=_("order"), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=_("product"), on_delete=models.CASCADE)
    quantity = models.IntegerField(_("quantity"), default=1)

    class Meta:
        verbose_name = _("order item")
        verbose_name_plural = _("order items")
        # два одинаковых продукта внутри одного заказа не должны существовать:
        unique_together = ("order", "product")

    def __str__(self):
        return f"Id: {self.id}| Q: {self.quantity}"

    # метод, чтобы посчитать количество каждого продукта
    @property
    def total_price(self):
        return self.product.price * self.quantity