import json
from django.http import HttpResponse
from ratelimit import rate_limit_by_ip

@rate_limit_by_ip()
def index(request):
    return HttpResponse("It worked!", status=200)

    
