import django_filters
from django_filters import FilterSet
from products.models import *


class ProductListFilter(FilterSet):
    category_ids = django_filters.CharFilter(method='filter_category_ids')

    class Meta:
        model = Product
        # сортировка по возрастанию\убыванию
        fields = {
            'price': ['gte', 'lte']
        }

    def filter_category_ids(self, queryset, name, value):
        return queryset.filter(category__id__in=value.split(','))




