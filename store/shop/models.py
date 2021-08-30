from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    list_name = models.CharField(max_length=50)


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200, default='', null=True, blank=True)
    image = models.ImageField(upload_to='uploads/products/')
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_category_id(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()
