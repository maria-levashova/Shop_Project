from django.urls import path

from common.views import *

# ConfigView.as_view() - запустить view, as_view() - т.к. является классом
urlpatterns = [
    path('config/', ConfigView.as_view(), name='config'),
]
