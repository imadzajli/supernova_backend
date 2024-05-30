from django.urls import path

from .views import *



urlpatterns = [
    path('',home),
    path('getStarted',getstarted),
    path('to_mqtt',mqtt),
    path('display_text_to_robot',send_text_to_robot),
    path('send_mouvement_to_robot',send_mouvement_to_robot),
    path('send_gps_robot',send_gps_to_robot),
]