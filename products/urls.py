from django.urls import path
from products.views import *

urlpatterns = [
    path('main-categories/', MainCategoryListAPIView.as_view(), name='main-categories'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('product-list/', ProductListAPIView.as_view(), name='product-list'),
    # path('product-categories/', ProductCategoryListAPIView.as_view(), name='product-category-list'),
    path('orders/', CreateOrderAPIView.as_view(), name='create-order'),
    path('', ProductFilterListAPIView.as_view(), name='product-filter'),

]