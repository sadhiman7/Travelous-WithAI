from django.db import models

# Create your models here.

class Tours(models.Model):
    tour_id = models.AutoField
    destination = models.CharField(max_length=50)
    dn = models.CharField(max_length=20)
    image = models.ImageField(upload_to='img/tours', default="")
    sdesc = models.CharField(max_length=300)
    state = models.CharField(max_length=20)
    about = models.TextField(max_length=10000)
    price = models.IntegerField(max_length=7)
    category = models.CharField(max_length=20)


    def __str__(self):
        return self.destination


class PlaceToVisit(models.Model):
    name = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    desc = models.CharField(max_length = 1000)


class HowToReach(models.Model):
    destination = models.CharField(max_length=50)
    via = models.CharField(max_length=10)
    desc = models.CharField(max_length=1000)

class Bookings(models.Model):
    email = models.CharField(max_length=30)
    destination = models.CharField(max_length=50)
    bookingdate = models.CharField(max_length=10)
    dob = models.DateTimeField()
    adults = models.IntegerField(max_length=2)
    children = models.IntegerField(max_length=2)


class blogs(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=20)
    body = models.TextField(max_length=5000)
    destination = models.CharField(max_length=20)
    imagebig = models.ImageField(upload_to='img/blog', default="")
    imagesmall1 = models.ImageField(upload_to='img/blog', default="")
    imagesmall2 = models.ImageField(upload_to='img/blog', default="")
    nViews = models.IntegerField()
    #sdesc = models.CharField(max_length=500)

class comments(models.Model):
    body= models.CharField(max_length=500)
    author = models.CharField(max_length=20)
    blogid = models.ForeignKey(blogs, on_delete=models.CASCADE)

