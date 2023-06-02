from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Product(models.Model):
    GENDER = (
        ('M', 'M'),
        ('F', 'F'),
        ('U', 'U'),
    )

    id = models.AutoField(primary_key=True)
    product = models.CharField(max_length=100)  # Changed field name from 'product'
    purchase = models.CharField(max_length=100)
    sale = models.CharField(max_length=100)
    qty = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, null=True, choices=GENDER)
    notes = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to='media/pdf_files/', null=True, blank=True)


    
    def __str__(self):
        return self.product
