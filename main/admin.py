from django.contrib import admin
from .models import ContactMessage
from .models import Payment
admin.site.register(Payment)
admin.site.register(ContactMessage)
# Register your models here.
