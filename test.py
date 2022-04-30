import requests

BASE = "http://127.0.0.1:5000/"

response = requests.put(BASE + "customer_login", {"customer_first_name":"Loganand", "mobile_number_with_ctry_code":"917708896034"})
print(response.json()) # To convert the response object ot JSON format