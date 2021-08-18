from django.db import models

class User(models.Model):
    kakao        = models.IntegerField()
    name         = models.CharField(max_length=300)
    birthday     = models.DateField(null=True)   
    thumbnail    = models.CharField(max_length=2000)
    is_host      = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'