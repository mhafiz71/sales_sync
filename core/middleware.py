from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = ['login', 'logout']
        self.exempt_prefixes = ['/admin', '/media/', '/static/']

    def __call__(self, request):
        if request.user.is_authenticated:
            return self.get_response(request)

        if any(request.path.startswith(prefix) for prefix in self.exempt_prefixes):
            return self.get_response(request)

        try:
            url_name = request.resolver_match.url_name
            if url_name in self.exempt_urls:
                return self.get_response(request)
        except AttributeError:
            return self.get_response(request)

        login_url = reverse('login')
        return redirect(f'{login_url}?next={request.path}')