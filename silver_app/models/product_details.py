from django.db import models
from product import Product


class ProductDetails(models.Model):
    product = models.ForeignKey(Product)
    timestamp = models.DateField(auto_now_add = True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    url = models.URLField()
    source = models.TextField()
    class Meta:
        app_label = "silver_app"
