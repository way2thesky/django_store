from django.urls import path

from middlewares.auth import auth_middleware
from .views import Basket

app_name = 'basket'

urlpatterns = [
    path('basket/', auth_middleware(Basket.as_view()), name='basket'),
]
