from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

'''
The first line says that we'll use Flask to render a template, redirecting to another url, and creating a URL.
The second line says we'll use PyMongo to interact with our Mongo database.
The third line says that to use the scraping code, we will convert from Jupyter notebook to Python.
'''
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

'''
app.config["MONGO_URI"] tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL.
"mongodb://localhost:27017/mars_app" is the URI we'll be using to connect our app to Mongo. 
This URI is saying that the app can reach Mongo through our localhost server, using port 27017, using a database named "mars_app".
'''

@app.route("/") #Hompage
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

@app.route("/scrape") #Scraping route
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

'''
@app.route(“/scrape”) defines the route that Flask will be using. 
This route, “/scrape”, will run the function that we create just beneath it.
we assign a new variable that points to our Mongo database: mars = mongo.db.mars

.update_one(query_parameter, {"$set": data}, options)

Here, we're inserting data, but not if an identical record already exists. In the query_parameter, we can specify a field (e.g. {"news_title": "Mars Landing Successful"}), in which case MongoDB will update a document with a matching news_title. Or it can be left empty ({}) to update the first matching document in the collection.

Next, we'll use the data we have stored in mars_data. The syntax used here is {"$set": data}. This means that the document will be modified ("$set") with the data in question.

Finally, the option we'll include is upsert=True. This indicates to Mongo to create a new document if one doesn't already exist, and new data will always be saved (even if we haven't already created a document for it).

The entire line of code looks like this: mars.update_one({}, {"$set":mars_data}, upsert=True).

Finally, we will add a redirect after successfully scraping the data: return redirect('/', code=302). This will navigate our page back to / where we can see the updated content.



'''

if __name__ == "__main__":
   app.run()