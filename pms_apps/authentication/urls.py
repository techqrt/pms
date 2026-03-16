from django.urls import path
from pms_apps.authentication.controller import AuthController

urlpatterns = [
    path("register/", AuthController.register, name="register"),
    path("login/", AuthController.login, name="login"),
    path("login-with-username/", AuthController.login_with_username, name="login_with_username"),
    path("verify-otp/", AuthController.verify_otp, name="verify_otp"),
]
