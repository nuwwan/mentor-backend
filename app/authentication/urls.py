from django.urls import path

from .views import protected_view, login_view, register_view

urlpatterns = [
    path("login", login_view, name="login_view"),
    path("register", register_view, name="register_view"),
    path("user", protected_view, name="get_user"),
]
