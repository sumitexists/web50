from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class Listing(models.Model):
    categories = [
    ("ELEC", "Electronics"),
    ("FASH", "Fashion"),
    ("HOME", "Home & Garden"),
    ("COLL", "Collectibles & Art"),
    ("MOTO", "Motors"),
    ("SPRT", "Sporting Goods"),
    ("TOYS", "Toys & Hobbies"),
    ("BUSI", "Business & Industrial"),
    ("MUSC", "Music"),
    ("MOVI", "Movies & TV"),
    ("GAME", "Video Games & Consoles"),
    ("HLTH", "Health & Beauty"),
    ("BABY", "Baby"),
    ("PETS", "Pet Supplies"),
    ("BOOK", "Books, Comics & Magazines"),
    ("JEWL", "Jewelry & Watches"),
    ("INST", "Musical Instruments & Gear"),
    ("ANTI", "Antiques"),
    ("REAL", "Real Estate"),
    ("SERV", "Specialty Services"),
    ("NCTL" , "No Category Listed")
]
    heading = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    base_bid = models.IntegerField()
    current_bid = models.IntegerField(default=0)
    number_of_bid = models.IntegerField(default=0)
    description = models.TextField()
    image = models.ImageField(upload_to='listings')
    category = models.CharField(max_length=5, choices=categories)
    listing_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_user")
    watchlist_user = models.ManyToManyField(User , related_name='watchlist_user', null=True)
    def __str__(self):
        return f"{self.name} - base bid {self.base_bid}" 
