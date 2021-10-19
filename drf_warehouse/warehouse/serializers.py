from rest_framework import serializers

from .models import Author, Book, Order, OrderItem, Genre


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['url', 'id', 'name']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'author', 'genre', 'title', 'description', 'language', 'pages', 'image',
                  'slug', 'price', 'isbn', 'created', 'available', 'quantity']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'book', 'price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source="order_item_set", many=True)

    class Meta:
        model = Order
        fields = ['id', 'first_name', 'last_name', 'email', 'status', 'items']

    def create(self, validated_data):
        valid_data = validated_data.pop('order_item_set')
        order = Order.objects.create(**validated_data)
        order_items_serializer = self.fields['order_items']
        for each in valid_data:
            each['order'] = order
        order_items_serializer.create(valid_data)
        return order, valid_data


class GetRequestSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)