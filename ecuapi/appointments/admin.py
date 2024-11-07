from django.contrib import admin

# Register your models here.
from .models import Appointment, Customer, Stylist

admin.site.register(Appointment)
admin.site.register(Customer)
admin.site.register(Stylist)
