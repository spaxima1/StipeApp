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

db=get_database()
#create or connect  Table for  ids payment
idsTable=db['idsTable']


#connect to stripe web site and payment 
@app.route('/charge', methods=['POST'])
def charge():

    api_key = 'sk_test_51Kux0CJJ4eit2YqKLw6BGayeA4eHnQi8FqNwieOuDmA7QLNuP7KH482k1oqmQwN8D7Mh6E5MpMpg3nL1VXrGd20J00qxt0GavI'
    token = request.form.get('stripeToken')
    Mony=request.form.get("PaymentMoney")
    
    headers = {'Authorization' : f'Bearer {api_key}'}
    data = {
            'amount' : Mony, 
            'currency' : 'usd', 
            'description' : 'Another Charge', 
            'source' : token
        }
    
    #send post request to stripe web site 
    requestStripe = requests.post('https://api.stripe.com/v1/charges', headers=headers, data=data)
    idPayment={"id":requestStripe.json()['id']}
    idsTable.insert_one(idPayment)

    return jsonify(requestStripe.json())

@app.route('/ids')
def TablesID():
    item_details=idsTable.find()
    data={}
    count=0
    for item in item_details:
        data[count]=item['id']
        count+=1
    return render_template('Tableids.html',data=data)