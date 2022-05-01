from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy

import os
from dotenv import load_dotenv
load_dotenv()

my_number = os.environ.get('my_number')
account_sid = os.environ.get('account_sid')
auth_token = os.environ.get('auth_token')

import twilio
from twilio.rest import Client
import random

app = Flask(__name__)
api = Api(app) # Initializes Restful Api
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class customer_model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(100),nullable=False)
    otp = db.Column(db.Integer, nullable=False)
    is_verified = db.Column(db.String(1),nullable=False)

    def __repr__(self):
        return f'Customer ID = {self.id}\nCustomer First Name = {self.first_name}\nCustomer Last Name = {self.last_name}\nMobile Number = {self.mobile_number}\nOTP = {self.otp}\nIs_Verified = {self.is_verified}\n'        
    
#db.create_all() # Run only once to create the Database, since we dont want to overwrite data

customer_login_put_arguments = reqparse.RequestParser()
customer_login_put_arguments.add_argument('customer_first_name', type=str, help='Customer First Name is Mandatory', required=True) # help argument is to send user an error messgae if the argument is not passed
customer_login_put_arguments.add_argument('customer_last_name', type=str, help='Customer Last Name is Mandatory', required=True) 
customer_login_put_arguments.add_argument('mobile_number_with_ctry_code', type=str, help='Customer Mobile Number is Mandatory', required=True)

resource_fields = {
'id': fields.Integer,
'first_name': fields.String,
'last_name': fields.String,
'mobile_number': fields.String,
'is_verified':fields.String
}# To define how to serialize the record from DB(which would be returned as Instance)

class customer_get(Resource): # customer_login class will Inherit from Resource
    @marshal_with(resource_fields)
    def get(self,customer_id):
        result = customer_model.query.filter_by(id = customer_id).first()
        if not result:
            abort(404, message='Invalid Customer Id, please try again')
        return result, 201

api.add_resource(customer_get,'/customer_login/<int:customer_id>')

class customer_login(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return {'welcome_text' : 'Welcome to Bank'} # Returned object should be serializable( can be converted to JSON format like Javascript objects)
       
    @marshal_with(resource_fields)    
    def put(self):
        # Add row to Database
        args = customer_login_put_arguments.parse_args()
        result = 1
        while result == 1:
            random_customer_id = random.randint(10000,99999)
            result = customer_model.query.filter_by(id=random_customer_id).first()
            if not result:
                result = 0
        otp = random.randint(1000,9999)
        customer = customer_model(id= random_customer_id, first_name=args.customer_first_name, last_name=args.customer_last_name, mobile_number=args.mobile_number_with_ctry_code, otp=otp, is_verified='N')
        db.session.add(customer)
        db.session.commit()

        #twilio
        client = Client(account_sid, auth_token)
        message = client.messages.create(
                body='Hello ' + args.customer_first_name + ' ' + args.customer_last_name + '\nYour OTP is ' + str(otp) +'\nYour Customer ID is ' + str(random_customer_id),
                from_=my_number,
                to=args.mobile_number_with_ctry_code
            )
        return customer, 201
api.add_resource(customer_login,'/customer_login') # Register customer_login as a resource.. the '/' is the default/home URL

customer_verification_put_arguments = reqparse.RequestParser()
customer_verification_put_arguments.add_argument('customer_id', type=int, help='Customer ID is Mandatory', required=True) 
customer_verification_put_arguments.add_argument('customer_otp', type=int, help='OTP is Mandatory', required=True) 

class customer_verification(Resource):
    @marshal_with(resource_fields)
    def put(self):
        args = customer_verification_put_arguments.parse_args()
        result = customer_model.query.filter_by(id = args.customer_id).first()
        if result:
            if result.otp == args.customer_otp:
                print ('You are verified now: ' + result.first_name.upper() + ' ' + result.last_name.upper() + '\n Welcome to Our Bank')
                result.otp, result.is_verified = 0, 'Y'
                print(result)                    
                db.session.commit()
                if result.mobile_number[1] == '1': # US (+1xxxxxxxx)
                    print(result.first_name + ' ' + result.last_name + ' ! You are verified that you are in USA')
                    return result, 201
                elif result.mobile_number[1:3] == '91': # India (+91xxxxxxxxxx)
                    print(result.first_name + ' ' + result.last_name + ' ! You are verified that you are in India')
                    return result, 201
            else:
                abort(401,message='Invalid OTP, please try again')
        else:
            abort(404,message='Invalid Customer ID, please try again')
        
api.add_resource(customer_verification,'/customer_verification')

if __name__ == '__main__':
    app.run(debug=True)
