from flask import Flask, jsonify, request
import pymongo
from pymongo import MongoClient
from flask_cors import CORS
from bson import ObjectId

app = Flask(__name__)
cors = CORS(app) #permits the api to act on the browser

ids = [] #list that holds each event ID

@app.route('/')
def index():
    return "Hello, World!"
@app.route('/calendar/api/v1.0/events/all', methods=['GET'])
def get_eventList():
    cluster = MongoClient("mongodb+srv://Alanjcortez:T574KLirNgSf6n2w@agora-hbyod.mongodb.net/Agora_events?retryWrites=true&w=majority&serverSelectionTimeoutMS=360000")
    db = cluster["Agora_events"]
    collection = db["Agora_events"]
    eventList = []
    results = collection.find({}) #gets all the events from database
    for result in results:
        result['_id'] = str(result['_id']) #turns the obj id into a string
        eventList.append(result)

    return jsonify({'events': eventList})


@app.route('/calendar/api/v1.0/events', methods=['POST'])
def create_event(): 
    cluster = MongoClient("mongodb+srv://Alanjcortez:T574KLirNgSf6n2w@agora-hbyod.mongodb.net/Agora_events?retryWrites=true&w=majority&serverSelectionTimeoutMS=360000")
    db = cluster["Agora_events"]
    collection = db["Agora_events"]
    

    if not request.json: # If the data isn't there
        return "Error: You fucked up"
    event = { #creates an event based on what's in the body's JSON
        'name': request.json.get('name', ""),
        'description': request.json.get('description', ""),
        'location': request.json.get('location', ""),
        'organizer': request.json.get('organizer', ""),
        'date': request.json.get('date', "")
    }
    collection.insert_one(event) #adds event into the database
    #updateEventId(event)
    return jsonify({'Message': 'Event added'}), 201


@app.route('/calendar/api/v1.0/events/<string:name>', methods=['PUT']) 
def update_event(name):
    cluster = MongoClient("mongodb+srv://Alanjcortez:T574KLirNgSf6n2w@agora-hbyod.mongodb.net/Agora_events?retryWrites=true&w=majority&serverSelectionTimeoutMS=360000")
    db = cluster["Agora_events"]
    collection = db["Agora_events"]

    result = collection.find_one({"name": name}) #finds the event base 
    result['_id'] = str(result['_id']) #turns the obj id into a string
    event = {
        'name': request.json.get('name', result['name']),
        'description': request.json.get('description', result['description']),
        'location': request.json.get('location', result['location']),
        'organizer': request.json.get('organizer', result['organizer']),
        'date': request.json.get('date', result['date'])
    }

    #updates the event information in the database
    collection.update_one({"name": name}, {"$set": {"name": event['name'], "description": event['description'], "location": event['location'], "organizer": event['organizer'], "date": event['date']}})
    return jsonify({'Message': 'Event {} is updated'.format(name)}), 200



@app.route('/calendar/api/v1.0/events/<string:ID>', methods=['DELETE']) 
def remove_event(ID):
    cluster = MongoClient("mongodb+srv://Alanjcortez:T574KLirNgSf6n2w@agora-hbyod.mongodb.net/Agora_events?retryWrites=true&w=majority&serverSelectionTimeoutMS=360000")
    db = cluster["Agora_events"]
    collection = db["Agora_events"]
    
    collection.delete_one({"_id": ObjectId(ID)}) #delete the event based on the ID ObjetctId(ID)
    return jsonify({'Message': 'Event has been removed'})

if __name__ == '__main__':
    app.run(debug=True)

