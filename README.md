
VEHICLES
====================================
GET

URL:http://localhost:8000/vehicles/24
====================================
POST

URL:http://localhost:8000/vehicles/
DATA:{
    "vehicle_model_id": {
    	"name": "320d",
    	"brand": "BMW"
    },
    "km": 3500,
    "plate": "07ctu12",
    "vehicle_id_number": "123s456ASD789S",
    "colour": "Blue",
    "is_deleted": false,
    "is_active": true
}
===================================
PUT

URL:http://localhost:8000/vehicles/25/
DATA:{
    "vehicle_model_id": {
    	"name": "E46",
    	"brand": "BMW"
    },
    "km": 220000,
    "plate": "35abk12",
    "vehicle_id_number": "852S456ASD789S",
    "colour": "Blue",
    "is_deleted": false,
    "is_active": true
}
==================================
PATCH

URL:http://localhost:8000/vehicles/25/
DATA:{
    "vehicle_model_id": {
    "name": "320d",
    "brand": "BMW"
    },
    "colour":"Black"
}
=================================
DELETE

URL:http://localhost:8000/vehicles/25/
=================================


VEHICLE MODELS
===============================
GET

URL:http://localhost:8000/vehiclemodels
===============================
POST

URL:http://localhost:8000/vehiclemodels/
DATA:{
    "name": "320d",
    "brand": "BMW"
    }
===============================
PUT

URL:http://localhost:8000/vehiclemodels/5/
DATA:{
    "name": "320d",
    "brand": "BMW"
    }
===============================
PATCH

URL:http://localhost:8000/vehiclemodels/5/
DATA:{"name": "320d",}
===============================
DELETE

URL:http://localhost:8000/vehiclemodels/5/
===============================

REDIS MONITOR
![redis-monitor](https://user-images.githubusercontent.com/32904056/128599176-c94a795c-3d84-4d6c-b69e-68b10bd918ec.png)
