from urllib.request import Request
from django.http import HttpRequest
def token_cookie_to_header_middleware(get_response):

    def middleware(request: Request):
        for key, value in request.session.items():
            print('{} => {}'.format(key, value))

        return get_response(request)

    return middleware
