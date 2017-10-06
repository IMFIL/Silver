from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=30)
    image = models.URLField()
    description = models.TextField()
    category = models.ForeignKey(Category)
