import requests
import json

# POST Client for Delivery Fee Calculator created by Anton Backman

URL = 'http://localhost:5000/delivery_app'  # URL to the local backend server

# Change the order details here
order_details = {
    "cart_value": 790, 
    "delivery_distance": 1301, 
    "number_of_items": 7, 
    "time": "2024-01-12T16:30:00Z"
    }

headers = {'Content-Type': 'application/json'}

try:
    response = requests.post(URL, json.dumps(order_details), headers=headers)
    response_data = response.json()
    print(response_data)
except Exception as e:
    print(f"There was an error sending the POST request! {e}")
