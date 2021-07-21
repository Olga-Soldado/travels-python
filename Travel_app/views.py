from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render,redirect
# Create your views here.
from .models import *
import bcrypt

# render home page
def home(request):
    return render(request, "index.html")

#process registration and redirect
def register(request):
    errors = User.objects.register(request.POST)
    if len(errors) > 0:
        for key,error in errors.items():
            messages.error(request, error)
        return redirect("/")
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create( password=pw_hash, name=request.POST['name'], username=request.POST['username'])
        request.session['user_id'] = user.id #generated by django
        request.session['username'] = user.username
        messages.success(request, "Registro Exitoso:)")
        return redirect("/travels")    

# process login info and redirect
def login(request):
    errors = User.objects.login(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect("/")
    else:
        user = User.objects.filter(username=request.POST['username'])
        if len(user) < 1:
            messages.error(request, "Ya se encuentra registrado este usuario.")
            return redirect("/")
        
        if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
            print(f"LOG - Setting session value 'user_id' = {user[0].id}")
            request.session['user_id'] = user[0].id
            request.session['username'] = user[0].username
            return redirect("/travels")
        else:
            messages.error(request, "Contraseña incorrecta")
            return redirect("/")

# logout and redirect
def exit(request):
    request.session.clear()
    messages.success(request, "Sesion cerrada exitosamente!")
    print(f"Redireccionando a home")  
    return redirect("/")

#redirigir  a la pagina travels.
def main(request):
    if 'user_id' not in request.session:
        messages.error(request, "Acceso denegado")
        return redirect("/")
    context = {
        "user_id" : request.session['user_id'],
        "username": request.session['username'] ,
        "viajes": Travel.objects.all(),
    }
    print(f"Redirigiendo a la pagina principal de viajes.")
    return render(request, "menu.html", context)
def new(request):
    return render(request,"crear.html")

def create(request):
    Travel.objects.create(
        destination = request.POST['destination'],
        description = request.POST['description'],
        travel_date_from = request.POST['travel_date_from'],
        travel_date_to = request.POST['travel_date_to'],
    )
    messages.success(request, 'Se creo un nuevo viaje')
    return redirect("/travels")

def shows(request,id):
    context = {
        "user_id" : request.session['user_id'],
        "username": request.session['username'] ,
        "inf": Travel.objects.get(id=id),
    }
    return render(request, "informacion.html", context)