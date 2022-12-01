from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class auction_listing(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.TextField()
    category = models.TextField()

class bid(models.Model):
    auction_id = models.IntegerField()
    user = models.CharField(max_length=500)
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)

class comment(models.Model):
    auction_id = models.IntegerField()
    message = models.TextField()

class watchlist(models.Model): 
    auction_id = models.IntegerField()
    user = models.CharField(max_length=500)
   
