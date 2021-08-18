from django.db       import models
from users.models    import User
from products.models import Product
from core.models     import TimeStampModel

class Booking(TimeStampModel):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    product      = models.ForeignKey(Product, on_delete=models.CASCADE)
    check_in     = models.DateField()
    check_out    = models.DateField()
    head_count   = models.IntegerField()
    total_price  = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'bookings'