from flask import Flask, render_template, request,jsonify
import requests 

#create app for run server 
app = Flask(__name__)
app.config['DEBUG'] = True

#create root rout 
@app.route('/')
def index():
    #render html file in template folder
    return render_template('index.html')

#create or Connect to DataBase 
def get_database():
    from pymongo import MongoClient

    CONNECTION_STRING = 'mongodb://127.0.0.1:27017/'
    client = MongoClient(CONNECTION_STRING)

    return client['StripeTables']

