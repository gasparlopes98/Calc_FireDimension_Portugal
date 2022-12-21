from django.http import HttpResponse
from .calculate_info import get_info,calculate_index

def index(request):
    calculate_index()
    return HttpResponse(get_info())