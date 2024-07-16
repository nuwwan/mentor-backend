from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .utils import generate_jwt_token, decode_jwt_token
from .models import AuthUser


@api_view(["POST"])
def register_view(request):
    data = request.data
    email = data.get("email")
    password = data.get("password")
    firstname = data.get("firstname")
    lastname = data.get("lastname")
    if email and password and firstname:
        # create the User
        try:
            # check if the user already exists
            user = AuthUser.objects.filter(email=email)
            if user:
                return Response(
                    {"message": "User already exists. Please login"},
                    status=status.HTTP_409_CONFLICT,
                )
            user = AuthUser.objects.create_user(
                email=email,
                password=password,
                first_name=firstname,
                last_name=lastname,
            )
            user.save()
            return Response({"status": "Success"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(
                {"status": "Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        return Response({"status": "Error"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_view(request):
    data = request.data
    email = data.get("email")
    password = data.get("password")
    user = authenticate(email=email, password=password)
    if user:
        token = generate_jwt_token(user=user)
        return Response({"jwt": token}, status=status.HTTP_200_OK)
    return Response(
        {"message": "User is not authenticated"}, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected_view(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return Response(
            {"error": "Authorization header missing"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token = auth_header.split(" ")[1]
    payload = decode_jwt_token(token)
    if payload:
        user_id = payload.get("id")
        user = AuthUser.objects.get(id=user_id)
        return Response({"email": user.email}, status=status.HTTP_200_OK)
    return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
