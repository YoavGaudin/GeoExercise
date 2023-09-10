from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Country, City

admin.site.register(Country)
admin.site.register(City)
