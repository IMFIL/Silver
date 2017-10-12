from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    class Meta:
        app_label = "silver_app"
        
