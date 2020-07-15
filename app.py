from flask import Flask, render_template, request,jsonify
from flask_cors import CORS, cross_origin
import requests
import pymongo
import os

from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup
import requests


app = Flask(__name__)
CORS(app) 

#dbConn = pymongo.MongoClient("mongodb://localhost:27017/")

#dbname='crawlerDB'
#db = dbConn[dbname]

@app.route('/', methods=['GET', 'POST']) # To render Homepage
@cross_origin()
def index():
    if (request.method == 'POST'):
        
        
        searchString = request.form['content'].replace(" ","")

        
        # collection=db[searchString]
        # reviews = collection.find({})

        # if reviews.count() > 0:
        #     return render_template('results.html',reviews=reviews)
        # else:
        inputstring = "https://www.flipkart.com/search?q="
        outputstring = inputstring+searchString
        source = requests.get(outputstring).text
        flipkart_html  = BeautifulSoup(source,'lxml')
        reviews = []

        for article in flipkart_html.find_all("div", {"class": "_3O0U0u"}):

            try:
                name = article.find("div",{"class": "_3wU53n"}).text
            except :
                name = None
                    
            try:
                cost = article.find("div",{"class": "_1vC4OE _2rQ-NK"}).text
            except :
                cost = None    
                        
            try:
                desc = article.find("ul",{"class": "vFw0gD"}).text
            except :
                desc = None    
                

            mydict = { "Name": name, "Cost": cost, "Description": desc}
            reviews.append(mydict)
            # collection.insert_one(mydict)     
                

        print(reviews)

        return render_template('results.html', reviews=reviews)

    else:
        return render_template('index.html')        

port = int(os.getenv("PORT"))
if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0',port=port)
