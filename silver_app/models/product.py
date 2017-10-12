from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=30)
    image = models.URLField()
    category = models.ForeignKey("Category")

    class Meta:
        app_label = "silver_app"
