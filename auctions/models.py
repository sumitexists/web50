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
    status = [
        ('True' , 'Biding ongoing'), ("False", "Biding is over")
    ]
    heading = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    base_bid = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='listings')
    category = models.CharField(max_length=5, choices=categories)
    listing_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_user")
    watchlist_user = models.ManyToManyField(User , related_name='watchlist_user')
    status = models.CharField(max_length=5 , choices=status , default='True')
    number_of_bid = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.name} - by {self.listing_user}" 


class comments(models.Model):
    commented_user = models.ForeignKey(User, related_name = 'commented_user', on_delete=models.CASCADE)
    product = models.ForeignKey(Listing, related_name='product', on_delete=models.CASCADE)
    comment = models.TextField()

    def __string__(self):
        return f'{self.commented_user.username}: comment on listing {self.product}' 
    
class winner(models.Model):
    listing = models.ForeignKey(Listing , on_delete=models.CASCADE , related_name='listing_name')
    winner = models.ForeignKey(User, on_delete=models.CASCADE , related_name="winning_user")
    current_bid = models.IntegerField()


    def __str__(self):
        return f'{self.winner} is winning the listing {self.listing}'