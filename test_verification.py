import requests

BASE = 'http://127.0.0.1:5000/'

response = requests.put(BASE + 'customer_verification', {'customer_id':XXXXX,'customer_otp':XXXX})
print(response.json())