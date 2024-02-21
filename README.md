# Delivery Fee Calculator created by Anton Backman

## Description

- Programmed in Visual Studio Code.
- HTTP API created with the Flask framework.
- Dynamic calculation of delivery fees based on the parameters cart value, delivery distance, number of items and rush hour.
- Configuration variables to tweak behaviour of calculator for future updates and maintenance.

# Versions used

Python 3.10.10
Flask 3.0.1

You may need to install a few modules to fix the import errors.

# To install the missing module(s) write the following in the terminal

pip install flask
pip install datetime
pip install requests
pip install re
pip install json

# How to use

To use the calculator you need to run delivery_fee_calculator.py first to start the server.
After starting the server you can send a POST request to the URL: http://localhost:5000/delivery_app in the example format:

order_details = {
    "cart_value": 790, 
    "delivery_distance": 1301, 
    "number_of_items": 7, 
    "time": "2024-01-12T16:30:00Z"
    }

I have also created post_client.py to help with this, where you can edit the values to test the HTTP API.

# Testing

I have created a testing class using unittest to make sure all of the functions work as intended.
To run the test class simply write the command: python -m unittest test_delivery_fee_calculator.py in the terminal.
