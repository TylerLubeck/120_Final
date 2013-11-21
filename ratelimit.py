from django.core.cache import get_cache
from datetime import datetime as dt
from datetime import timedelta
cache = get_cache('rate_limiting')

def rate_limit_by_ip(limit_for=30, limit=1, how_many_hits=50, exception_list=[]):
    """
    Django decorator to limit how often an ip can acess a view.
    Args:
        limit_for      :: How long, in seconds, before access is regranted
        limit          :: How long, in seconds, before the limit is applied.
                          See 'how_many_hits'
        how_many_hits  :: How many hits are allowed in 'limit' seconds 
                          before the limit is applied
        exception_list :: A list of IPs to exclude
    Usage:
        @rate_limit_by_ip
        def my_view(request):
            #I am less likely to have excessive database hits due to DDOS or
            #shitty code

    """
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            remote_addr = request.META.REMOTE_ADDR

            if remote_addr in exception_list:
                return func(request, *args, **kwargs)

            count = cache.get(remote_addr)
            
            if count is None:
                d = {
                    'how_often' : 1,
                    'whenSeen' : dt.now(),
                    'allow_again' : None
                }
                cache.set(remote_addr, d, limit_for)
                return func(request, *args, **kwargs)
            
            else:
                count['how_often'] += 1
                
