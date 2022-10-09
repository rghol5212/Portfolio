from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(max_length=500, default="Tell us about your self")



class UserStat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    value = models.IntegerField(default=0)
    date_logged = models.DateTimeField(auto_now_add=True)


class Categories(models.Model):
    categories = (
        ("general", "General"),
        ("cars/trucks", "Cars/Trucks"),
        ("home furniture", "Home Furniture"),
        ("electronics", "Electronics"), 
        ("garden", "Garden"),
        ("animals", "Animals"),
        )
    category = models.CharField(max_length=17, choices=categories)




class ActiveListing(models.Model):
    name_of_listing = models.CharField(max_length=25, unique=True)
    start_price = models.IntegerField(default=0)
    description = models.CharField(max_length=300)
    created_date = models.DateTimeField(auto_now_add=True)
    categories = models.ForeignKey(Categories, default=1, on_delete=models.CASCADE)
    number_of_bids = models.IntegerField(default=0)
    highest_bidder = models.ForeignKey(User, default=None, blank=True, related_name='highest_bidder', null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', default="https://customercare.igloosoftware.com/.api2/api/v1/communities/10068556/previews/thumbnails/4fc20722-5368-e911-80d5-b82a72db46f2?width=820&height=680&crop=False")
    is_sold = models.BooleanField(default=False)
    upload_author = models.ForeignKey(User, related_name='upload_author', on_delete=models.CASCADE, null=True, default=None) 

    def __str__(self):
        return f"{self.name_of_listing} at the price of {self.start_price}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(ActiveListing, on_delete=models.CASCADE)


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(ActiveListing, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250)