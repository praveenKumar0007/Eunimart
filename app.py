from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app) # Initializes Restful Api

class customer_login(Resource): # customer_login class will Inherit from Resource
    def get(self):
        return {"data" : "Hello World"} # Returned object should be serializable( can be converted to JSON format like Javascript objects)

api.add_resource(customer_login,"/") # Register customer_login as a resource.. the "/" is the default/home URL

if __name__ == "__main__":
    app.run(debug=True)