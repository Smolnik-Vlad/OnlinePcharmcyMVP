from django.db import models

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
        return "http://127.0.0.1:8000/catalog/{}".format(self.pk)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        default_related_name = 'product'
        ordering = ["addition_date"]

    def __str__(self) -> str:
        return self.title


class Rating(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='rating')
    rating_set = models.JSONField(default=dict, blank=True)
    slug = models.SlugField(max_length=100, null=True, blank=True, editable=False)

    @property
    def average_rating(self) -> float:
        ratings = [rating for rating in self.rating_set.values()]
        return sum(ratings) / len(ratings) if len(ratings) > 0 else None


class Comments(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment')
    customer = models.ForeignKey('users.Customer', on_delete=models.CASCADE, related_name='comment', null=True,
                                 blank=True)
    changed_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    comment_field = models.TextField()
    checked = models.BooleanField(default=False)

    @property
    def commenters_name(self):
        return f"{self.customer.user.first_name}"

    def __str__(self) -> str:
        return self.product.title


class Tag(models.Model):
    tag = models.CharField
    product = models.ManyToManyField(Product,
                                     related_name="tags"
                                     )


