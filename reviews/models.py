from django.db       import models
from users.models    import User
from products.models import Product
from core.models     import TimeStampModel

class Review(TimeStampModel):        
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    product      = models.ForeignKey(Product, on_delete=models.CASCADE)    
    score        = models.DecimalField(max_digits=3, decimal_places=2)
    comment      = models.TextField(null=True)

    class Meta:
        db_table = 'reviews'