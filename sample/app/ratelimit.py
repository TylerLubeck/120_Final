from django.core.cache import get_cache
from functools import wraps
from django.utils.decorators import available_attrs
import logging
from django.http import HttpResponse
import json
import math
#Get a cache instance that is specific for our plugin
cache = get_cache('rate_limiting')

def rate_limit_by_ip(how_many_hits=50, in_how_long=1, exception_list=[], uid=None):
    """
    Django decorator to limit how often an ip can acess a view.
    Args:
        how_many_hits  :: How many hits are allowed in 'in_how_long' 
                          seconds before the limit is applied
        in_how_long    :: If there are 'how_many_hits' in this many seconds,
                          BOOM limited
        exception_list :: A list of IPs to exclude
        uid            :: A value to look for in the request to use as a 
                          unique identifier for a request. If not set, the
                          requestor's IP address is used
    Usage:
        @rate_limit_by_ip
        def my_view(request):
            #I am less likely to have excessive database hits due to DDOS or
            #shitty code

    """
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            remote_addr = None
            if uid is None:
                remote_addr = request.META.get('REMOTE_ADDR', None)
                uid = 'REMOTE_ADDR'
            else:
                remote_addr = request.REQUEST.get(uid, None)
            if remote_addr is None:
                error = {'error': 'Your request did not include a value for the unique id: ' + uid}
                return HttpResponse(json.dumps(d), status=400, content_type="application/json")
            cache_key = func.__name__ + '_' + str(remote_addr)
            cache_key = str(cache_key)
            retVal = None
            #Allow for exceptions
            #cache.clear()
            if remote_addr in exception_list:
                retVal = func(request, *args, **kwargs)
            count = cache.get(cache_key)
            #We haven't seen them before
            if count is None:
                # Figure out how frequently a hit would have to occur in
                # order to hit the limit
                cacheTime = how_many_hits / in_how_long
                cacheTime = float(in_how_long) / float(how_many_hits)
                #Put them in the cache
                #Adjust caching time so we are caching in seconds and not
                #   fractions of seconds
                cacheTime = math.floor(cacheTime)
                if cacheTime < 1:
                    cacheTime = 1
                cache.set(cache_key, 'cached', cacheTime)
                #Allow them in to the function
                retVal = func(request, *args, **kwargs)
            
            #We've seen them in the limit time, so sucks to be you
            else:
                #429 is the error code for 'Too Many Requests'
                d = {'error': "You've hit your rate limit"}
                retVal = HttpResponse(json.dumps(d), content_type="application/json", status=429)
            return retVal
        return inner
    return decorator


