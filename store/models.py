from django.db import models

class product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='store/images', default="")
    description = models.TextField(max_length=2000)
    brand = models.CharField(max_length=100,default="Unknown Brand")
    stock = models.IntegerField()
    def __str__(self):
        return self.name
# Create your models here.
