from django.shortcuts import render, redirect
from .models import * 
from django.contrib import messages 

def index(request):
    # messges1 = Message.objects.all()
    # User.objects.all().delete() clears users if stuff isn't working
    return render(request, "blackBelt_app/index.html")

def register(request): 

    response = User.objects.register(
        request.POST["first"],
        request.POST["last"],
        request.POST["username"],
        request.POST["email"],
        request.POST["dob"],
        request.POST["password"], 
        request.POST["confirm"]

    )
    print "WHAT"
 
    if response["valid"]: 
        request.session["user_id"] = response["user"].id 
        return redirect("/home")
    else: 
        for error_message in response["errors"]: 
            messages.add_message(request, messages.ERROR, error_message)
        return redirect("/")

def login(request): 
    response = User.objects.login(
        request.POST["email"],
        request.POST["password"]
    )
    if response["valid"]: 
        request.session["user_id"] = response["user"].id 
        return redirect("/home")
    else: 
        for error_message in response["errors"]: 
            messages.add_message(request, messages.ERROR, error_message)
        return redirect("/")

def home(request): 
    if "user_id" not in request.session: 
        return redirect("/")
    
    user = User.objects.get(id=request.session["user_id"])
    # my_trips = User.objects.get(id=request.session["user_id"])
    other_trips = Trip.objects.exclude(id=request.session["user_id"])
    joinedTrips = User.objects.get(id=request.session['user_id'])
    
    context = {
        "user" : user.first_name,
        "my_trips" : user.traveler.all(),
        "other_trips" : other_trips,
        "joinedTrips" : joinedTrips.cotraveler.all()
    }

    print joinedTrips.cotraveler.all(),"HELLLOOOOO"
    for x in joinedTrips.cotraveler.all():
        print x.traveler_id

    print other_trips
    for x in other_trips:
        print x.description

    return render(request, "blackBelt_app/home.html", context)

def logout(request): 
    request.session.clear()
    return redirect("/")

def dashboard(request):
    return redirect("/home")

def addTrip(request):
    if "user_id" not in request.session: 
        return redirect("/")
    
    return render(request, "blackBelt_app/addTrip.html")

def createTrip(request):

    destination = request.POST['destination']
    description = request.POST['description']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    traveler = User.objects.get(id=request.session['user_id'])

    trip = Trip.objects.add(destination, description, start_date, end_date, traveler)

    if trip[0] == False:
        print "dont know how to do this part apparently"
        return redirect ("/addTrip")
    else:
        return redirect('/home')

def tripInfo(request, kittycatlicklick):
    trip = Trip.objects.get(id=kittycatlicklick)
    user = User.objects.get(id=request.session["user_id"])
    cotravelers = FavoriteTrip.objects.filter(trip=kittycatlicklick)

    context = {
        "user" : user.first_name,
        "trip" : trip,
        "cotravelers" : cotravelers
    }

    return render(request, "blackBelt_app/tripInfo.html", context)

def joinTrip(request, kittysaurus):

    trip = Trip.objects.get(id=kittysaurus)
    user = User.objects.get(id=request.session["user_id"])

    FavoriteTrip.objects.create(trip=trip, traveler_id=request.session["user_id"])

    return redirect("/home")

def remove(request, id):
    trip = Trip.objects.get(id=id)
    myTrips = FavoriteTrip.objects.filter(trip=id).delete()

    return redirect("/home")