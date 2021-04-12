from django.db import models

# Create your models here.
from account.models import Account


class Villa(models.Model):
    villa_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    TYPE_CHOICES = [
        ('Coastal', 'Coastal'),
        ('Urban', 'Urban'),
        ('Wild', 'Wild'),
        ('Mountainous', 'Mountainous'),
        ('Desert', 'Desert'),
        ('Rural', 'Rural'),
        ('Suburban', 'Suburban'),
    ]
    type = models.CharField(max_length=12, choices=TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    price_per_night = models.IntegerField(default=0)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    area = models.IntegerField()
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    number_of_bathrooms = models.IntegerField(default=1)
    number_of_bedrooms = models.IntegerField(default=1)
    number_of_single_beds = models.IntegerField(default=1)
    number_of_double_beds = models.IntegerField(default=1)
    number_of_showers = models.IntegerField(default=1)

    def __str__(self):
        return self.name + ", Owner: " + self.owner.first_name + " " + self.owner.last_name


class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=40, null=True, blank=True)
    villa = models.ForeignKey(Villa, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='villas/images/', blank=True, null=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.title + ' ' + self.image.url
