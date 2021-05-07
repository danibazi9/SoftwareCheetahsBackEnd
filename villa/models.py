from django.db import models

# Create your models here.
from account.models import Account


class Facility(models.Model):
    facility_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=40, null=True, blank=True)
    image = models.ImageField(upload_to='villas/images/')
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"Image ID: {self.image_id}, Title: {self.title}"


class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='villas/documents/')

    def __str__(self):
        return f"Document ID: {self.document_id}"


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
        ('Motel', 'Motel'),
    ]
    type = models.CharField(max_length=12, choices=TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    price_per_night = models.IntegerField()
    images = models.ManyToManyField(Image, blank=True)
    facilities = models.ManyToManyField(Facility, blank=True)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    postal_code = models.CharField(max_length=10, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    area = models.IntegerField()
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    max_capacity = models.IntegerField()
    number_of_bathrooms = models.IntegerField(default=1)
    number_of_bedrooms = models.IntegerField(default=1)
    number_of_single_beds = models.IntegerField(default=1)
    number_of_double_beds = models.IntegerField(default=1)
    number_of_showers = models.IntegerField(default=1)
    documents = models.ManyToManyField(Document, blank=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name + ", Owner: " + self.owner.first_name + " " + self.owner.last_name

<<<<<<< HEAD

class Calendar(models.Model):
    calendar_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    villa = models.ForeignKey(Villa, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField() 
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.villa.name + ", Customer: " + self.customer.__str__()
