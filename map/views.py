from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from map.models import User, Incident, editRequest

def index(request):
    cases = Incident.objects.all()
    return render(request, "map/index.html", {
        "cases": cases,
    })


# Get case data from database.
def mapData(request):
    cases = Incident.objects.all()
    if request.method == "GET":
        return JsonResponse([case.serialize() for case in cases], safe=False)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "map/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "map/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "map/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "map/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "map/register.html")


# Save a new incident to database.
def logCase(request):
    if request.method == "POST":
        typeOf = request.POST["type"]
        htmlDateTime = request.POST["datetime"]
        pythonDateTime = datetime.strptime(htmlDateTime, '%Y-%m-%dT%H:%M')
        latitude = request.POST["latitude"]
        longitude = request.POST["longitude"]
        description = request.POST["description"]
        newCase = Incident(typeOf=typeOf, timestamp=pythonDateTime, lat=latitude, long=longitude, description=description)
        newCase.save()
        return render(request, "map/thankyou.html")
    else:
        return render(request, "map/logcase.html")

# Thank you page after logging a case.
def thankYou(request):
    return render(request, "map/thankyou.html")


# Save an edit request to database.
def requests(request):
    user = request.user
    if request.method == "POST":
        description = request.POST["description"]
        targetPost = request.POST["target-id"]
        newRequest = editRequest(targetPost=targetPost, description=description)
        newRequest.save()
        inc = Incident.objects.get(pk=targetPost)
        inc.beingEdited = True
        inc.save()
        requests = editRequest.objects.all()
        return HttpResponseRedirect(reverse("index"))
    else:    
        requests = editRequest.objects.all()
        return render(request, "map/requests.html", {
            "requests": requests,
            "user": user,
        })    

# Get an individual case.
def requestACase(request, case_id):
    if request.method == "GET":
        case = Incident.objects.get(pk=case_id)
        return JsonResponse(case.serialize(), safe=False)

# Get an edit request.
def requestAnEdit(request, case_id):
    if request.method == "GET":
        case = editRequest.objects.get(targetPost=case_id)
        return JsonResponse(case.serialize(), safe=False)

# Accept a request to edit a case.
@csrf_exempt
def acceptAnEdit(request, case_id):
    case = Incident.objects.get(pk=case_id)
    if request.method == "PUT":
        req = editRequest.objects.get(targetPost=case_id)
        req.delete()
        data = json.loads(request.body)
        if data.get("description") is not None:
            case.description = data["description"]
            case.beingEdited = False
            case.save()
        return JsonResponse({"result": "Incident has been updated"})

def checkAuthentication(request):
    user = request.user
    return JsonResponse({"result": user.is_authenticated})

# Reject a request to edit a case.
def rejectAnEdit(request, case_id):
    case = Incident.objects.get(pk=case_id)
    case.beingEdited = False
    case.save()
    req = editRequest.objects.get(targetPost=case_id)
    req.delete()
    return JsonResponse({"result": "Request has been rejected"})
