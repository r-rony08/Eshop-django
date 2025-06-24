from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete

# Create your models here.

class Categories(models.TextChoices):
    ELECTRONIC = 'electronic'
    LAPTOPS ='laptops'
    ARTS = 'arts'
    HOME = 'home'
    FOOD = 'food'
    KITCHEN = 'kitchen'

class Product(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,blank=True,null=True)
    image=models.JSONField()
    description=models.TextField()
    specifications=models.TextField()
    price=models.FloatField()
    weight=models.FloatField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    color=models.CharField(max_length=255)
    brand=models.CharField(max_length=255)
    brand_model=models.CharField(max_length=255)
    seo_title=models.CharField(max_length=255)
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name='added_by_user_id_products')
    Categories = models.CharField(max_length=30, choices=Categories.choices)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='images')
    image = models.ImageField(upload_to='products/')

@receiver(post_delete, sender=ProductImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)


class Review(models.Model):
     product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='reviews')
     user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
     rating = models.IntegerField(default=0)
     comment = models.TextField(default="", blank=False)
     created_at=models.DateTimeField(auto_now_add=True)

     def __str__(self):
         return str(self.comment)
