from django.db import models


class Payment(models.Model):
    email = models.EmailField()
    plan = models.CharField(max_length=100)
    amoount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.email} - {self.amoount}'

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, default="New Contact Form")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.email} - {self.subject}"
# Create your models here.
