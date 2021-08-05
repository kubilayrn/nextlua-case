from django.db import models

# Create your models here.

class VehicleModel(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    
    def __str__(self):
        return self.brand + ' ' +self.name

class Vehicle(models.Model):
    
    km = models.IntegerField(default=0,blank=True) 
    plate = models.CharField(max_length=128,blank=True,unique=True)
    vehicle_id_number = models.CharField(max_length=100)
    colour = models.CharField(max_length=100)
    vehicle_model_id = models.ForeignKey(VehicleModel,on_delete=models.CASCADE,related_name='vehicle')
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Vehicles"
    
    def __str__(self):
        return self.plate
