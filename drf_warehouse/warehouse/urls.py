from django.urls import include, path

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'authors', views.AuthorViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'order_items', views.OrderItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include(
        'rest_framework.urls',
        namespace='rest_framework')
         ),
    path('recieve/', views.get_request)
]
