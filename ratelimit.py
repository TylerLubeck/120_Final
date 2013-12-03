from django.core.cache import get_cache
from functools import wraps
from django.utils.decorators import available_attrs
import logging
from django.http import HttpResponse

logger = logging.getLogger('django.request')
#Get a cache instance that is specific for our plugin
cache = get_cache('rate_limiting')

def rate_limit_by_ip(how_many_hits=50, in_how_long=1, exception_list=[]):
    """
    Django decorator to limit how often an ip can acess a view.
    Args:
        how_many_hits  :: How many hits are allowed in 'in_how_long' 
                          seconds before the limit is applied
        in_how_long    :: If there are 'how_many_hits' in this many seconds,
                          BOOM limited
        exception_list :: A list of IPs to exclude
    Usage:
        @rate_limit_by_ip
        def my_view(request):
            #I am less likely to have excessive database hits due to DDOS or
            #shitty code

    """
    def decorator(func):
        print 'SOME SHIT BAD'
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            print "IN THE INNER PART"
            remote_addr = request.META['REMOTE_ADDR']
            cache_key = func.__name__ + '_' + str(remote_addr)
            cache_key = str(cache_key)
            print 'KEY:" '+ cache_key + '"'
            retVal = None
            #Allow for exceptions
            if remote_addr in exception_list:
                retVal = func(request, *args, **kwargs)

            count = cache.get(cache_key)
            print 'COUNT IS', count
            #We haven't seen them before
            if count is None:
                # Figure out how frequently a hit would have to occur in
                # order to hit the limit
                cacheTime = how_many_hits / in_how_long
                print cacheTime
                #Put them in the cache
                cache.set(cache_key, 'cached', cacheTime)
                print cache.get(cache_key) 
                #Allow them in to the function
                retVal = func(request, *args, **kwargs)
            
            #We've seen them in the limit time, so sucks to be you
            else:
                #429 is the error code for 'Too Many Requests'
                retVal = HttpResponse(status=429)
            return retVal
        return inner
    return decorator


