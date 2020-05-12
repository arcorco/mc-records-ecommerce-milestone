from django.db import models

# Create your models here.

class Product(models.Model):
    GENRE_CHOICES = (('RO','Rock'),
    ('PO', 'Pop'),
    ('RB', 'R&B'),
    ('ME', 'Metal'),
    ('CL', 'Classical'),
    ('JA', 'Jazz'),
    ('DA', 'Dance'),
    ('CO', 'Country'),
    ('RE', 'Reggae'),
    ('FO', 'Folk'), 
    ('IN', 'Indie'),
    ('AL', 'Alternative'))

    OFFER_CHOICES = (('N', ('No')),
                     ('Y', ('Yes')))

    product_type = models.CharField(max_length=20, default="")
    album = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    genre = models.CharField(choices=GENRE_CHOICES, max_length=2)
    release_date = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cover = models.ImageField(upload_to='images')
    offer = models.CharField(choices=OFFER_CHOICES, max_length=1)

class Tracks(models.Model):
    album = models.ForeignKey('Product', on_delete=models.CASCADE)
    track = models.CharField(max_length=200)
    length = models.TimeField()
