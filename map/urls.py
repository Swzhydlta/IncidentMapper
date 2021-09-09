from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("logcase", views.logCase, name="logCase"),
    path("thankyou", views.thankYou, name="thankYou"),
    path("mapdata", views.mapData, name="mapData"),
    path("requests", views.requests, name="requests"),
    path("requestACase/<int:case_id>", views.requestACase, name="requestACase"),
    path("requestAnEdit/<int:case_id>", views.requestAnEdit, name="requestAnEdit"),
    path("acceptAnEdit/<int:case_id>", views.acceptAnEdit, name="acceptAnEdit"),
    path("checkAuthentication", views.checkAuthentication, name="checkAuthentication"),
    path("rejectAnEdit/<int:case_id>", views.rejectAnEdit, name="rejectAnEdit"),
]