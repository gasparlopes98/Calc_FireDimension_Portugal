from django.http import HttpResponse
from .calculate_info import get_info, calculate_index
from rest_framework.decorators import api_view
import json


@api_view(['GET', 'POST', 'DELETE'])
def index(request):
    calculate_index()
    get_info()
    json1 = {
        "latitude": 37.17259764813775,
        "longitude": -7.516036839467642,
        "resources_by_area": [
            {
                "area": "Viana do Castelo",
                "trucks": 5,
                "jipe": 10,
                "hely": 0
            },
            {
                "area": "Vila Real",
                "trucks": 5,
                "jipe": 10,
                "hely": 0
            }
        ]

    }

    return HttpResponse(json.dumps(json1))
