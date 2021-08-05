from  rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from . import models


class VehicleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VehicleModel
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    vehicle_model_id = VehicleModelSerializer(read_only=True)
    class Meta:
        model = models.Vehicle
        fields = '__all__'

