from django.db                 import models
from django.db.models.deletion import CASCADE
from users.models              import User
from core.models               import TimeStampModel

class Product(TimeStampModel):
    name           = models.CharField(max_length=300)
    head_count     = models.IntegerField()
    user           = models.ForeignKey(User,on_delete=models.CASCADE)
    latitude       = models.DecimalField(max_digits=9, decimal_places=6)
    longitude      = models.DecimalField(max_digits=9, decimal_places=6)
    price          = models.DecimalField(max_digits=10, decimal_places=2)    
    address        = models.CharField(max_length=500)
    detail_address = models.CharField(max_length=500,null=True)
    grade          = models.DecimalField(max_digits=10,decimal_places=2)
    description    = models.TextField(null=True)

    class Meta:
        db_table = 'products'

class Image(TimeStampModel):
    product    = models.ForeignKey(Product,on_delete=models.CASCADE)
    image      = models.CharField(max_length=2000)

    class Meta:
        db_table = 'images'

class Category(models.Model):
    product       = models.ForeignKey(Product, on_delete=models.CASCADE)     
    big_address   = models.CharField(max_length=500)
    small_address = models.CharField(max_length=500)
    created_at    = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'categories'   
