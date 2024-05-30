from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import paho.mqtt.client as mqtt
import json,os
import firebase_admin
from firebase_admin import credentials,firestore
from datetime import datetime


current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "mqtt.json")
key_path = os.path.join(current_dir,'key.json')

cred = credentials.Certificate(key_path)
firebase_admin.initialize_app(cred)

db = firestore.client()




mqtt_file = open(file_path,"r")
mqtt_data = json.load(mqtt_file)

broker = mqtt_data["broker"]
port = mqtt_data["port"]  

last_mvmt =(0,0)

client = mqtt.Client()



def send_to_mqtt(broker,portt,topic,message):
    def on_connect(client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        
        client.publish(topic, message)
        print(f"Message '{message}' sent to topic '{topic}'")

    
    

   
    client.on_connect = on_connect

  
    client.connect(broker, port, 60)

    client.loop_start()


    client.loop_stop()
    client.disconnect()


def home(request):
    
    return render(request,"index.html")

def getstarted(request):
    return render(request,"Started.html")

def mqtt(request):
    return JsonResponse({"data":"imadxt"})


def send_text_to_robot(request):

    topic = mqtt_data["topics"]['display']
    message = request.GET.get('paragraph')

    #print(f"topic : {topic}\n message : {message}")

    send_to_mqtt(broker,port,topic,message)

    return render(request,"Started.html")

def send_mouvement_to_robot(request):
    if request.method == "POST":
        data = json.loads(request.body)
        angle = data.get('angle')
        force = data.get('force')
        topic = mqtt_data["topics"]['mouvement']

        message = {
            "angle" : angle,
            "force" : force
        }
        message_json = json.dumps(message)
        send_to_mqtt(broker,port,topic,message_json)

        return JsonResponse({"data":angle,"force":force,"topic":topic,"message":message})

def send_gps_to_robot(request):

    topic = mqtt_data["topics"]['GPS']
    user = request.GET.get('name')
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')

    data = {
        "user" : user,
        "latitude" : latitude,
        "longitude" : longitude
    }

    json_data = json.dumps(data)

    send_to_mqtt(broker,port,topic,json_data)
    db.collection("EHTP_2024").add(data)



    return render(request,"Started.html")