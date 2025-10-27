from django.db import models


# Create your models here.
class plants(models.Model):
    Name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="images/")
    discount_price = models.FloatField(null=True)
    mrp = models.FloatField(null=True)
    discount = models.FloatField(null=True)
    rate = models.IntegerField(null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)


    def __str__(self):
        return self.Name
    
from django.contrib.auth.models import User
class cart(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE,db_column="uid")
    pid = models.ForeignKey(plants, on_delete=models.CASCADE,db_column="pid")
    qty = models.IntegerField(default=1)


class Order(models.Model):
    order_id = models.CharField(max_length=50)
    uid = models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid = models.ForeignKey(plants,on_delete=models.CASCADE,db_column="pid")
    qty = models.IntegerField(default=1)

class saved(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    pid = models.ForeignKey(plants, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.uid.username} saved {self.pid.Name}"



