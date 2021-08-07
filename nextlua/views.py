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

# Create your views here.
class VehicleViewSet(viewsets.GenericViewSet):

    queryset = models.Vehicle.objects.filter(is_active=True,is_deleted=False)
    serializer_class = serializers.VehicleSerializer

    def create(self,request,*args,**kwargs):
        
        vehicle = models.Vehicle(
            plate = request.data["plate"],
            km = request.data["km"],
            vehicle_id_number =request.data["vehicle_id_number"],
            vehicle_model_id=models.VehicleModel.objects.get(name = request.data["vehicle_model_id"]['name'], brand = request.data["vehicle_model_id"]["brand"]),
            colour =  request.data["colour"],
            is_active = request.data["is_active"],
            is_deleted = request.data["is_deleted"]
        )
        vehicle.save()
        serializer = self.get_serializer(vehicle)
        key = "vehicles_" + str(serializer.data.get('id'))
        redis_instance.set(key,json.dumps(serializer.data))
        
        return Response(serializer.data)

    def list (self,request,*args,**kwargs):
        
        key = "vehicles_*"
        keys = redis_instance.keys(key)
        pks=[]
        redis_datas=[]
        if len(keys)>0:
            for i in keys:
                pk=str(i).split('_')
                pks.append(int(pk[1].replace("'","")))
            
                tmp=redis_instance.get(i)
                redis_datas.append(json.loads(tmp))
            
            excludes=self.queryset.exclude(pk__in=pks)

            #db query results added redis_datas
            for i in excludes:
                index = {   "id": i.id,
                            "vehicle_model_id": {
                                "id": i.vehicle_model_id.id,
                                "name": i.vehicle_model_id.name,
                                "brand": i.vehicle_model_id.brand
                            },
                            "km": i.km,
                            "plate": i.plate,
                            "vehicle_id_number": i.vehicle_id_number,
                            "colour": i.colour,
                            "is_deleted": i.is_deleted,
                            "is_active": i.is_active,
                            "created_on": str(i.created_on),
                            "modified_on": str(i.modified_on)
                }
                redis_instance.set("vehicles_" + str(i.id),json.dumps(index))
                redis_datas.append(index)

            page = self.paginate_queryset(redis_datas)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(redis_datas, many=True)
        else:
            queryset = self.filter_queryset(self.get_queryset()) 
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
        return Response(sorted(serializer.data, key=lambda x: x["id"], reverse=False))

    def retrieve(self, request, *args, **kwargs):
        # key ile cache kontrol ediliyor.cache'de var ise cacheden yanıt dönülüyor.
        # Yok ise db den dönen sonuç cache yazılıyor ardından response dönülüyor.
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

        vehicle = models.Vehicle.objects.get(pk=kwargs['pk'])
        data =request.data

        vehicle.plate = data.get("plate")
        vehicle.km = data.get("km")
        vehicle.vehicle_id_number = data.get("vehicle_id_number",vehicle.vehicle_id_number)
        vehicle.vehicle_model_id = models.VehicleModel.objects.get(
                                                                name = data["vehicle_model_id"]['name'],
                                                                brand = data["vehicle_model_id"]["brand"])
        vehicle.colour =  data.get("colour")
        vehicle.is_active = data.get("is_active")
        vehicle.is_deleted = data.get("is_deleted")

        vehicle.save()
        serializer = self.serializer_class(vehicle)

        redis_instance.set(key, json.dumps(serializer.data))

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        key = "vehicles_" + kwargs['pk']
        value = redis_instance.get(key)
        if value:
            redis_instance.delete(key)

        vehicle = models.Vehicle.objects.get(pk=kwargs['pk'])
        data =request.data

        vehicle.plate = data.get("plate",vehicle.plate)
        vehicle.km = data.get("km",vehicle.km)
        vehicle.vehicle_id_number = data.get("vehicle_id_number",vehicle.vehicle_id_number)
        if data.get("vehicle_model_id"):
            vehicle.vehicle_model_id = models.VehicleModel.objects.get(
                                            name = data["vehicle_model_id"]['name'],
                                            brand = data["vehicle_model_id"]["brand"])
        else:
            vehicle.vehicle_model_id = vehicle.vehicle_model_id
        vehicle.colour =  data.get("colour",vehicle.colour)
        vehicle.is_active = data.get("is_active",vehicle.is_active)
        vehicle.is_deleted = data.get("is_deleted",vehicle.is_deleted)

        vehicle.save()
        serializer = self.serializer_class(vehicle)

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

class VehicleModelViewSet(viewsets.GenericViewSet):
    queryset = models.VehicleModel.objects.all()
    serializer_class = serializers.VehicleModelSerializer

    def create(self,request,*args,**kwargs):

        vehicle_model = models.VehicleModel(
            name = request.data["name"],
            brand = request.data["brand"]
        )
        vehicle_model.save()
        serializer=self.get_serializer(vehicle_model)
        key = "vehiclemodel_"+ str(serializer.data.get('id'))
        redis_instance.set(key,json.dumps(serializer.data))
        return Response(serializer.data) 

    def list (self,request,*args,**kwargs):
        key = "vehiclemodel_*"
        keys = redis_instance.keys(key)
        pks=[]
        redis_datas=[]
        if len(keys) > 0:
            for i in keys:
                pk=str(i).split('_')
                pks.append(int(pk[1].replace("'","")))
            
                tmp=redis_instance.get(i)
                redis_datas.append(json.loads(tmp))
            
            excludes=self.queryset.exclude(pk__in=pks)

            #db query results added redis_datas
            for i in excludes:
                index={"id":i.id,"name":i.name,"brand":i.brand}
                redis_instance.set("vehiclemodel_"+str(i.id),json.dumps(index))
                redis_datas.append(index)

            # serializer = self.serializer_class(data=list(redis_datas),many=True)
            # serializer.is_valid(raise_exception=True)
            page = self.paginate_queryset(redis_datas)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(redis_datas, many=True)
        else:
            # serializer=self.serializer_class(data=list(self.queryset.values()),many=True)
            # serializer.is_valid(raise_exception=True) 
            queryset = self.filter_queryset(self.get_queryset()) 
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
        return Response(sorted(serializer.data, key=lambda x: x["id"], reverse=False))

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

        vehicle_model = models.VehicleModel.objects.get(pk=kwargs['pk'])
        data =request.data

        vehicle_model.name = data.get("name",vehicle_model.name)
        vehicle_model.brand = data.get("brand",vehicle_model.brand)

        vehicle_model.save()
        serializer = self.serializer_class(vehicle_model)

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

    