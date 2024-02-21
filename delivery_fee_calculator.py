import math
from datetime import datetime, time
from flask import Flask, request, jsonify
import re

# Delivery Fee Calculator created by Anton Backman

# Variables to easily change the behaviour of the app
MAX_DELIVERY_FEE = 1500             # Max possible delivery fee
ITEM_SURCHARGE = 50                 # Item surcharge added for every additional item after 4 items
BULK_SURCHARGE = 120                # The bulk surcharge added after 12 items
BASE_FEE = 200                      # Base delivery fee for the first 1000 meters
EXTRA_FEE = 50                      # Delivery fee added for every 500 meters after initial fee
RUSH_HOUR_MULTIPLIER = 1.2          # Rush hour multiplier added during the specified rush hours
START_OF_RUSH_HOUR = time(15, 0)    # Start time for rush hour
END_OF_RUSH_HOUR = time(19, 0)      # End time for rush hour

delivery_app = Flask(__name__)

@delivery_app.route("/delivery_app", methods=["POST"])
# Function for the API server
def API_server():
    try:
        data = request.get_json()  # Get JSON data from the request

        # Running checks on data in json payload to ensure valid values
        if not isinstance(data["cart_value"], (int)) or data["cart_value"] < 0:
            raise ValueError("Invalid value for cart_value")
        
        if not isinstance(data["delivery_distance"], int) or data["delivery_distance"] < 0:
            raise ValueError("Invalid value for delivery_distance")
        
        if not isinstance(data["number_of_items"], int) or data["number_of_items"] <= 0:
            raise ValueError("Invalid value for number_of_items")
        
        if not isinstance(data["time"], str) or not re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', data["time"]):
            raise ValueError("Invalid value for time. Must be in the format YYYY-MM-DDTHH:mm:ssZ.")

        # Parsing all the data in the json payload
        cart_value = data["cart_value"]
        delivery_distance = data["delivery_distance"]
        number_of_items = data["number_of_items"]
        time = data["time"]

        # Calling the function to calculate the delivery fee
        delivery_fee = calculate_delivery_fee(cart_value, delivery_distance, number_of_items, time)
        return jsonify({"delivery_fee": delivery_fee})
    
    # Sending back error messages to notify what went wrong
    except ValueError as ve:
        error = {"Something went wrong!": str(ve)}
        return jsonify(error), 400
    
    except Exception as e:
        error = {"Something went wrong!": str(e)}
        return jsonify(error), 500

# Main function responsible for calculation delivery fee
def calculate_delivery_fee(cart_value, delivery_distance, number_of_items, time):
    delivery_fee = 0

    # If the cart value is over 200 euro, delivery will always be free
    if cart_value >= 20000:
        return delivery_fee

    # Adding surcharge to total if cart value is under 10 euro
    delivery_fee += calculate_surcharge(cart_value)

    # Adding distance costs to total
    delivery_fee += calculate_delivery_distance(delivery_distance)

    # If delivery fee already is over 15 euro we return the max value
    if delivery_fee >= MAX_DELIVERY_FEE:
        return MAX_DELIVERY_FEE

    # Adding extra fee to total for orders with more than four items
    delivery_fee += calculate_number_of_items(number_of_items)

    # If delivery fee already is over 15 euro we return the max value
    if delivery_fee >= MAX_DELIVERY_FEE:
        return MAX_DELIVERY_FEE

    # Checking if order was placed during rush hour, and adding multiplier id function returns True
    if is_rush_hour(time):
        delivery_fee *= RUSH_HOUR_MULTIPLIER

    # Returning the smaller value between the calculated fee and the maximum fee
    return min(delivery_fee, MAX_DELIVERY_FEE)

# Function to calculate how much to add to delivery in case cart value is under 10 euro
def calculate_surcharge(cart_value):
    return max(0, 1000 - cart_value)

# Function that calculates the delivery distance fee, base fee is always added even if delivery distance is shorter than 1km
def calculate_delivery_distance(delivery_distance):
    delivery_fee = BASE_FEE

    if delivery_distance > 1000:
        # Rounding up to the nearest integer since delivery for 1001m and 1500m should be the same 
        delivery_fee += EXTRA_FEE * (math.ceil((delivery_distance - 1000) / 500))
    
    return delivery_fee

# Function to calculate extra fees for orders with more than 4 items
def calculate_number_of_items(number_of_items):
    delivery_fee = 0

    # If order has more than 4 items we add 50 cents for every additional item
    if number_of_items > 4:
        delivery_fee += ITEM_SURCHARGE * (number_of_items - 4)
    
    # If order has more than 12 items we add a single time bulk surcharge
    if number_of_items > 12:
        delivery_fee += BULK_SURCHARGE
    
    return delivery_fee

# Function to determine if order was placed during rush hour
def is_rush_hour(input_date):
    # Formatting input time to a datetime object
    current_date = datetime.strptime(input_date, "%Y-%m-%dT%H:%M:%SZ")

    # Checking if it is friday, friday corresponds with 4
    if current_date.weekday() == 4:
        current_time = current_date.time()
        # Checking if current time falls between the specified start and end of rush hour
        return START_OF_RUSH_HOUR <= current_time < END_OF_RUSH_HOUR
    
    return False

if __name__ == "__main__":
    delivery_app.run(port=5000)