from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from .manager import CustomUserManager

        
class User(AbstractUser):
    username = models.CharField(max_length=50, blank=True,  null=True )
    email = models.EmailField(unique=True)
    Otp = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)  # Adjust as per your field definition
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    def __str__(self):
        return self.email
    
class Category(models.Model):
    name = models.CharField(max_length=100, null=False)
    slug = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Tags(models.Model):
    name = models.CharField(max_length=100, null=False)
    slug = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    image =models.ImageField()
    stock = models.CharField(max_length=100)
    price = models.IntegerField(null=True, blank=True)
    slug = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

class ProductTags(models.Model):
    tags = models.ManyToManyField(Tags)
    product = models.ManyToManyField(Product, related_name='product_tag_set')
    created_at = models.DateTimeField(auto_now_add=True)
 
class CartProduct(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    total_amount =  models.IntegerField()
    slug = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    



    

