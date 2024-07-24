from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest

from rest_framework.exceptions import AuthenticationFailed

from .utils import decode_jwt_token
from .models import AuthUser


class JWTAuthBackend(BaseBackend):
    def authenticate(self, request: HttpRequest):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None
        try:
            prefix, token = auth_header.split(" ")
            if prefix.lower() != "bearer":
                raise AuthenticationFailed("Invalid token prefix")
        except ValueError:
            raise AuthenticationFailed("Invalid token header")

        # validate the jwt token
        payload = decode_jwt_token(token)
        if not payload:
            raise AuthenticationFailed("Invalid Token")

        # get the user
        try:
            user = AuthUser.objects.get(id=payload["id"])
        except AuthUser.DoesNotExist:
            raise AuthenticationFailed("User doesn't Exists")
        return (user, token)

    def authenticate_header(self, request):
        return "Bearer"
