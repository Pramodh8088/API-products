from django.db import models

class Product(models.Model):
    product_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    tags = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name