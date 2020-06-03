from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.

class Product(models.Model):
    GENRE_CHOICES = (('RO','Rock'),
    ('PO', 'Pop'),
    ('RB', 'R&B'),
    ('RH', 'Rap and Hip-Hop'),
    ('ME', 'Metal'),
    ('CL', 'Classical'),
    ('JA', 'Jazz'),
    ('DA', 'Dance'),
    ('CO', 'Country'),
    ('RE', 'Reggae'),
    ('FO', 'Folk'), 
    ('IN', 'Indie'),
    ('AL', 'Alternative'))

    product_type = models.CharField(max_length=20, default="")
    album = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    genre = models.CharField(choices=GENRE_CHOICES, max_length=2)
    release_date = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cover = CloudinaryField('image')

    def __str__(self):
        return "{0} - {1}".format(self.artist, self.album)

class Track(models.Model):
    album = models.ForeignKey(Product)
    number = models.IntegerField(default=0)
    track = models.CharField(max_length=200)
    length = models.TimeField()

    def __str__(self):
        return "{0} - {1}".format(self.album, self.track)