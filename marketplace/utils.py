def get_client_ip(request):
    """
    Extracts the visitor's real client IP address safely from request headers,
    accounting for reverse proxies (localtunnel, Nginx, Cloudflare, Render).
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # X-Forwarded-For may contain a comma-separated list of IPs.
        # The first IP is the original client IP.
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip
