from django.db import models
from django.db.models import Avg

from catalog.managers import ProductInStockManager


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    brand = models.CharField(max_length=100)
    expiration_date = models.DateField()
    addition_date = models.DateField(auto_now_add=True)
    barcode = models.CharField(max_length=50)
    amount = models.IntegerField()
    info = models.TextField(blank=True)

    # Product model managers
    objects = models.Manager()
    in_stock = ProductInStockManager()

    @property
    def is_in_stock(self) -> bool:
        return True if self.amount > 0 else False

    @property
    def url(self) -> str:
        """
        Returns product URL for SimpleProductSerializer.
        """
        return "http://127.0.0.1:8000/catalog/{}".format(self.id)

    @property
    def average_rating(self):
        average = self.rating.aggregate(average=Avg('rating'))['average']
        return average if average is not None else 0

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        default_related_name = 'product'
        ordering = ["addition_date"]

    def __str__(self) -> str:
        return self.title


class Rating(models.Model):
    RATING_CHOICES = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rating')
    customer = models.ForeignKey("users.Customer", on_delete=models.CASCADE, related_name='rating')
    rating = models.IntegerField(choices=RATING_CHOICES)


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment')
    customer = models.ForeignKey('users.Customer', on_delete=models.CASCADE, related_name='comment', null=True,
                                 blank=True)
    changed_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    comment_field = models.TextField()

    @property
    def commenters_name(self):
        return f"{self.customer.user.first_name}"

    def __str__(self) -> str:
        return self.product.title


class Tag(models.Model):
    title = models.CharField(max_length=20, default='', blank=True)
    product = models.ManyToManyField(Product,
                                     related_name="tags"
                                     )

    def __str__(self) -> str:
        return self.title