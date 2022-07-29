from urllib.request import Request
from django.http import HttpRequest
def token_cookie_to_header_middleware(get_response):

    def middleware(request: Request):
        if request.COOKIES.get('token') and request.headers.get('Authorization') is None:
            request.META['Authorization'] = f"Token {request.COOKIES['token']}"

        return get_response(request)

    return middleware