from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import User

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='hotels/', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Event(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='events', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} at {self.hotel.name}"

class Service(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='services', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.name} at {self.hotel.name}"

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.hotel.name}"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    room = models.ForeignKey(Room, related_name='reservations', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    services = models.ManyToManyField(Service, related_name='reservations', blank=True)
    user = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Reservation for {self.customer_name} in {self.room.name} ({self.status})"