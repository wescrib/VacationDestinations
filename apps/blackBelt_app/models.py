from __future__ import unicode_literals

from django.db import models
import re 
from datetime import datetime 
import bcrypt 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class TripManager(models.Manager):
    def add(self, destination, description, start_date, end_date, traveler):
        response1 = {
            "errors" : [],
            "valid" : True
        }

        if len(destination) < 1:
            response1["errors"].append("Destination is required")
        elif len(destination) < 2:
            response1["errors"].append("Destination is invalid")
        
        if len(description) < 1:
            response1["errors"].append("Description is required")
        elif len(description) < 5:
            response1["errors"].append("Description is invalid")
        
        if len(start_date) < 1: 
            response1["errors"].append("Start date is required")
        else: 
            date = datetime.strptime(start_date, '%Y-%m-%d')
            today = datetime.now()
            if date < today: 
                response1["errors"].append("Start date is invalid")

        if len(end_date) < 1: 
            response1["errors"].append("Start date is required")
        else: 
            date = datetime.strptime(end_date, '%Y-%m-%d')
            today = datetime.now()
            if date < today: 
                response1["errors"].append("End date is invalid")
        if len(response1["errors"]) > 0: 
            return False, response1 
        else:
            trip = Trip.objects.create(destination = destination, description = description, start_date = start_date, end_date = end_date, traveler = traveler)
            return True, trip

class UserManager(models.Manager): 
    def register(self, first, last, username, email, dob, password, confirm):
        response = {
            "valid" : True, 
            "errors" : [],
            "user" : None
        }

        if len(first) < 1: 
            response["errors"].append("First name is required")
        elif len(first) < 2: 
            response["errors"].append("First name must be 2 characters or longer")

        if len(last) < 1: 
            response["errors"].append("Last name is required")
        elif len(last) < 2: 
            response["errors"].append("Last name must be 2 characters or longer")

        if len(username) < 1: 
            response["errors"].append("Username is required")
        elif len(username) < 3: 
            response["errors"].append("Last name must be 3 characters or longer")

        if len(email) < 1: 
            response["errors"].append("Email is required")
        elif not EMAIL_REGEX.match(email): 
            response["errors"].append("Invalid Email")
        else: 
            email_list = User.objects.filter(email=email.lower())
            if len(email_list) > 0: 
                response["errors"].append("Email is already in use.")

        if len(dob) < 1: 
            response["errors"].append("Date of Birth is required")
        else: 
            date = datetime.strptime(dob, '%Y-%m-%d')
            today = datetime.now()
            if date > today: 
                response["errors"].append("Date of Birth must be in the past")

        if len(password) < 1: 
            response["errors"].append("Password is required")
        elif len(password) < 8: 
            response["errors"].append("Password must be 8 characters or longer")

        if len(confirm) < 1: 
            response["errors"].append("Confirm Password is required")
        if confirm != password: 
            response["errors"].append("Confirm Password must match password")

        if len(response["errors"]) > 0: 
            response["valid"] = False 
        else: 
            response["user"] = User.objects.create(
                first_name = first, 
                last_name = last,
                username = username, 
                email = email.lower(), 
                dob = date, 
                password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            )
        return response 

    def login(self, email, password): 
        response = {
            "valid" : True, 
            "errors" : [],
            "user" : None
        }

        if len(email) < 1: 
            response["errors"].append("Email is required")
        elif not EMAIL_REGEX.match(email): 
            response["errors"].append("Invalid Email")
        else: 
            email_list = User.objects.filter(email=email.lower())
            if len(email_list) == 0: 
                response["errors"].append("Email is already in use.")
        
        if len(password) < 1: 
            response["errors"].append("Password is required")
        elif len(password) < 8: 
            response["errors"].append("Password must be 8 character or longer")

        if len(response["errors"]) == 0:
            hashed_pw = email_list[0].password
            if bcrypt.checkpw(password.encode(), hashed_pw.encode()):
                response["user"] = email_list[0]
            else: 
                response["errors"].append("Password is incorrect")
        if len(response["errors"]) > 0:
            response ["valid"] = False 

        return response

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    dob = models.DateField()
    password = models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    traveler = models.ForeignKey(User, related_name="traveler")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

class FavoriteTrip(models.Model):
    traveler = models.ForeignKey(User, related_name = "cotraveler")
    trip = models.ForeignKey(Trip, related_name="trip")
    objects = TripManager()