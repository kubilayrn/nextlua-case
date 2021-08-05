from rest_framework import viewsets
from . import models
from . import serializers

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.response import Response


from api import settings
import redis
import json
# Connect to our Redis instance
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT, db=1)

# items = {}
# count = 0
# for key in redis_instance.keys("*"):
#     items[key.decode("utf-8")] = redis_instance.get(key)
#     count += 1

# Create your views here.
class VehicleViewSet(viewsets.ModelViewSet):
    queryset = models.Vehicle.objects.filter(is_active=True,is_deleted=False)
    serializer_class = serializers.VehicleSerializer

    def retrieve(self, request, *args, **kwargs):
        key="vehicles_"+ kwargs['pk']
        value = redis_instance.get(key)
        if value:
            serializer = self.serializer_class(json.loads(value))
        else:
            value = self.queryset.get(pk=kwargs['pk'])
            serializer = self.serializer_class(value)
            redis_instance.set(key, json.dumps(serializer.data))
        return Response(data=serializer.data)

    def update(self, request, *args, **kwargs):
        key = "vehicles_" + kwargs['pk']
        value = redis_instance.get(key)
        if value:
            redis_instance.delete(key)

        instance = models.Vehicle.objects.get(pk=kwargs['pk'])
        serializer = self.serializer_class(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        redis_instance.set(key, json.dumps(serializer.data))

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        key = "vehicles_" + kwargs['pk']
        value = redis_instance.get(key)
        if value:
            redis_instance.delete(key)

        instance = models.Vehicle.objects.get(pk=kwargs['pk'])
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        redis_instance.set(key, json.dumps(serializer.data))

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        key="vehicles_"+ kwargs['pk']
        instance = self.queryset.get(pk=kwargs['pk'])
        instance.is_active = False
        instance.is_deleted = True
        instance.save()

        value = redis_instance.get(key)        
        if value:
            redis_instance.delete(key)

        return Response(data='delete success')

class VehicleModelViewSet(viewsets.ModelViewSet):
    queryset = models.VehicleModel.objects.all()
    serializer_class = serializers.VehicleModelSerializer

    def retrieve(self, request, *args, **kwargs):
        key="vehiclemodel_"+ kwargs['pk']
        value = redis_instance.get(key)
        if value:
            serializer = self.serializer_class(json.loads(value))
        else:
            value = models.VehicleModel.objects.get(pk=kwargs['pk'])
            serializer = self.serializer_class(value)
            redis_instance.set(key, json.dumps(serializer.data))
        return Response(data=serializer.data)

    def update(self, request, *args, **kwargs):
        key = "vehiclemodel_" + kwargs['pk']
        value = redis_instance.get(key)
        if value:
            redis_instance.delete(key)

        instance = models.VehicleModel.objects.get(pk=kwargs['pk'])
        serializer = self.serializer_class(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        redis_instance.set(key, json.dumps(serializer.data))

        return Response(serializer.data) 

    def partial_update(self, request, *args, **kwargs):
        key = "vehiclemodel_" + kwargs['pk']
        value = redis_instance.get(key)
        if value:
            redis_instance.delete(key)

        instance = models.VehicleModel.objects.get(pk=kwargs['pk'])
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        redis_instance.set(key, json.dumps(serializer.data))

        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        key="vehiclemodel_"+ kwargs['pk']        

        instance = models.VehicleModel.objects.get(pk=kwargs['pk'])
        instance.delete()

        value = redis_instance.get(key)
        
        if value:
            redis_instance.delete(key)

        return Response(data='delete success')

    