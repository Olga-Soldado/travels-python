from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register', views.register),
    path('login', views.login),
    path('exit', views.exit), 
    path('travels', views.main),
    path('travels/new',views.new),
    path('travels/new/create',views.create),
    path('travels/<int:id>',views.shows),
    # , path('listUsers', views.listUsers)
    # , path('listAttendees', views.listAttendees)
    # , path('add', views.add)
    # , path('addTravel', views.addTravel)
    # , path('join/<int:id>', views.join)
    # , path('tripDetail/<int:id>', views.tripDetail)
]