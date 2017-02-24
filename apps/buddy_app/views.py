from django.shortcuts import render, redirect
from models import Users, Trips
from django.contrib import messages
import bcrypt
from datetime import datetime

def main(request):
    return render(request, 'index.html')

def validate(request):
    if request.method == "POST":
        myvalidation = Users.objects.regvalidation(request.POST)
        if len(myvalidation) > 0:
            for error in myvalidation:
                messages.error(request, error)
            return redirect('/main')
        else:
            hashpass = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            Users.objects.create(name=request.POST['name'], username=request.POST['username'], password=hashpass)
            loggeduser = Users.objects.get(username=request.POST['username'])
            request.session['logged'] = {
                'id': loggeduser.id,
                'name': loggeduser.name,
                'username': loggeduser.username
            }
            return redirect('/travels')

def login(request):
    myvalidation = Users.objects.loginvalidation(request.POST)
    if len(myvalidation) > 0:
        for error in myvalidation:
            messages.error(request, error)
        return redirect('/main')
    else:
        loggeduser = Users.objects.get(username=request.POST['username'])
        request.session['logged'] = {
            'id': loggeduser.id,
            'name': loggeduser.name,
            'username': loggeduser.username
        }
        return redirect('/travels')

def logout(request):
    del request.session['logged']
    return redirect('/main')

def travels(request):
    mytrips = Trips.objects.filter(usertrip=request.session['logged']['id'])|Trips.objects.filter(tripplanner=request.session['logged']['id'])
    alltrips = Trips.objects.all().exclude(tripplanner=request.session['logged']['id']).exclude(usertrip=request.session['logged']['id'])
    context = {
        'triplist' : mytrips,
        'alltriplist' : alltrips
    }
    return render(request, 'traveldash.html', context)

def add(request):
    return render(request, 'addtrip.html')

def posttrip(request):
    validtrip = Users.objects.tripvalidation(request.POST)
    if len(validtrip) > 0:
        for error in validtrip:
            messages.error(request, error)
        return redirect('/travels/add')
    else:
        currenttrip = Trips.objects.create(destination=request.POST['destination'], plan=request.POST['plan'], startdate=datetime.strptime((request.POST['startdate']), '%Y-%m-%d'), enddate=datetime.strptime((request.POST['enddate']), '%Y-%m-%d'), tripplanner=Users.objects.get(id=request.session['logged']['id']))
        return redirect('/travels')

def join(request, id):
    Users.objects.get(id=request.session['logged']['id']).travelbud.add(Trips.objects.get(id=id))
    return redirect('/travels')

def destination(request, tripid):
    tripinfo = Trips.objects.get(id=tripid)
    otherusers = Users.objects.filter(travelbud=tripid)
    context = {
        'currenttrip': tripinfo,
        'joiningtrip': otherusers
    }
    return render(request, 'destination.html', context)
