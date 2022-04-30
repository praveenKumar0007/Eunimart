from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app) # Initializes Restful Api

customer_login_put_arguments = reqparse.RequestParser()
customer_login_put_arguments.add_argument("customer_first_name", type=str, help="Customer First Name is Mandatory", required=True) # help argument is to send user an error messgae if the argument is not passed
customer_login_put_arguments.add_argument("customer_last_name", type=str, help="Customer Last Name is Mandatory", required=True) 
customer_login_put_arguments.add_argument("mobile_number_with_ctry_code", type=str, help="Customer Mobile Number is Mandatory", required=True)

class customer_login(Resource): # customer_login class will Inherit from Resource
    def get(self):
        return {"welcome_text" : "Welcome to Bank"} # Returned object should be serializable( can be converted to JSON format like Javascript objects)
    def put(self):
        args = customer_login_put_arguments.parse_args()
        return {"Login": args}
api.add_resource(customer_login,"/customer_login") # Register customer_login as a resource.. the "/" is the default/home URL

if __name__ == "__main__":
    app.run(debug=True)