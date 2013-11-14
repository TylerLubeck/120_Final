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
    
