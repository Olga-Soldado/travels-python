
from django.contrib.messages.api import error
from django.db import models

# Create your models here.
import re
from datetime import *

class UserManager(models.Manager):
    def register(self, postData):
        #RegEx for Password
        PASSWORD_REGEX = re.compile(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d,!@#$%^&*+=]{8,}$')
        FISRT_NAME_REGEX = re.compile(r'^[a-zA-Z0-9]+$')
        errors = {}

        # Validating Password
        if len(postData['password']) < 1:
            errors['password'] = 'Password is required!'
        elif not PASSWORD_REGEX.match(postData['password']):
            errors['password_valid'] = 'La password debe contener almenos un numero y una mayuscula!'

        if len(postData['password_confirm']) < 1:
            errors['password_confirm'] = 'Confirmacion de password es requerida!'
        elif postData['password_confirm'] != postData['password']:
            errors['passwords_match'] = 'No coinciden ambas password'
        # Validating Name 
        if len(postData['name']) < 2:
            errors["name"] = "El nombre no puede tener tan pocos caracteres"
        elif not FISRT_NAME_REGEX.match(postData['name']):
            errors["name"] = "El nombre debe contener solo letras" 
        # Validating user Name
        if len(postData['username']) < 2:
            errors["username"] = "El Username no puede tener tan pocos caracteres"
        elif not FISRT_NAME_REGEX.match(postData['username']):
            errors["username"] = "El Username debe contener solo letras"
        return errors

# Login Validation
    def login(self, postData):
        messages = []
        if len(postData['username']) < 1:
            messages.append('El username es requerido!')

        if len(postData['password']) < 1:
            messages.append('La password es requerida!')
        return messages
class User(models.Model):
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    def __repr__(self):
        return f"<User object: {self.name}>"

class Travel(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    users = models.ManyToManyField(User, related_name="trips")
    travel_date_from = models.DateTimeField()
    travel_date_to = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #objects = TripManager()