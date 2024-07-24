from django.db import models

# Create your models here.

# model for soil moisture data


class SoilData(models.Model):
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    temperature = models.FloatField()
    humidity = models.FloatField()
    soil_texture = models.CharField(max_length=100)
    rainfall = models.FloatField()
    soil_moisture = models.FloatField()
    comment = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.date} {self.time} - {self.location} - Soil Moisture: {self.soil_moisture}"
