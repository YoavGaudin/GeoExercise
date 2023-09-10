from django.db import models

# Create your models here.


class Country(models.Model):
    country_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    city_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)

    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='cities')

    class Meta:
        unique_together = [['name', 'country']]

    def __str__(self):
        return self.name
