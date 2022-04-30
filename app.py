from flask import Flask
from flask_restful import Api, Resource, reqparse

import os
from dotenv import load_dotenv
load_dotenv()

my_number = os.environ.get("my_number")
account_sid = os.environ.get("account_sid")
auth_token = os.environ.get("auth_token")

import twilio
from twilio.rest import Client
import random

customers = {}
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
        random_customer_id = random.randint(10000,99999)
        otp = random.randint(1000,9999)
        client = Client(account_sid, auth_token)
        message = client.messages.create(
                body='Hello ' + args.customer_first_name + ' ' + args.customer_last_name + '\nYour OTP is ' + str(otp) +'\nYour Customer ID is ' + str(random_customer_id),
                from_=my_number,
                to=args.mobile_number_with_ctry_code
            )
        customers[random_customer_id] = args
        customers[random_customer_id]["otp"] = otp
        customers[random_customer_id]["customer_id"] = random_customer_id
        print(customers)
        return {"Login": args,"customer_id":random_customer_id, "status":200}
api.add_resource(customer_login,"/customer_login") # Register customer_login as a resource.. the "/" is the default/home URL

customer_verification_put_arguments = reqparse.RequestParser()
customer_verification_put_arguments.add_argument("customer_id", type=int, help="Customer ID is Mandatory", required=True) 
customer_verification_put_arguments.add_argument("customer_otp", type=int, help="OTP is Mandatory", required=True) 

class customer_verification(Resource):
    def put(self):
        args = customer_verification_put_arguments.parse_args()
        if args.customer_id in customers:
            if customers[args.customer_id]["otp"] == args.customer_otp:
                print ("You are verified now: " + customers[args.customer_id].customer_first_name + " " + customers[args.customer_id].customer_last_name + "\n Welcome to Our Bank")
                if customers[args.customer_id]["mobile_number_with_ctry_code"][1] == "1": # US (+1xxxxxxxx)
                    return {"message": customers[args.customer_id].customer_first_name.upper() + " " + customers[args.customer_id].customer_last_name.upper() + "! You are verified that you are from USA. Please Submit your First Name, Last Name, Father's Name, DOB, Permanent Address, Current Address to the Bank"}
                elif customers[args.customer_id]["mobile_number_with_ctry_code"][1:3] == "91": # India (+91xxxxxxxxxx)
                    return {"message": customers[args.customer_id].customer_first_name.upper() + " " + customers[args.customer_id].customer_last_name.upper() + "! You are verified that you are from India. Please Submit your Name, Surname, Family Name, Father's Name, DOB, Permanent Address,Current Address to the Bank"}
            else:
                return {"data" : "Invalid OTP","status":401}
        else:
            return {"data" : "Invalid Customer ID","status":404}
        
api.add_resource(customer_verification,"/customer_verification")

if __name__ == "__main__":
    app.run(debug=True)
