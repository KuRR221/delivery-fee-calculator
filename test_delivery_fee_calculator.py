import unittest
from delivery_fee_calculator import calculate_surcharge, calculate_delivery_distance, calculate_number_of_items, calculate_delivery_fee, is_rush_hour

# Test class for Delivery Fee Calculator created by Anton Backman

class test_delivery_fee_calc(unittest.TestCase):

    # Testing surcharge function
    def test_calculate_surcharge(self):
        result_1 = calculate_surcharge(790)
        self.assertEqual(result_1, 210)

        result_2 = calculate_surcharge(1320)
        self.assertEqual(result_2, 0)

        result_3 = calculate_surcharge(0)
        self.assertEqual(result_3, 1000)

        result_4 = calculate_surcharge(320)
        self.assertEqual(result_4, 680)

        result_5 = calculate_surcharge(990)
        self.assertEqual(result_5, 10)
    
    # Testing delivery distance function
    def test_calculate_delivery_distance(self):
        result_1 = calculate_delivery_distance(975)
        self.assertEqual(result_1, 200)

        result_2 = calculate_delivery_distance(1500)
        self.assertEqual(result_2, 250)

        result_3 = calculate_delivery_distance(1501)
        self.assertEqual(result_3, 300)

        result_4 = calculate_delivery_distance(6742)
        self.assertEqual(result_4, 800)

        result_5 = calculate_delivery_distance(2000)
        self.assertEqual(result_5, 300)

    # Testing number of items function
    def test_calculate_number_of_items(self):
        result_1 = calculate_number_of_items(4)
        self.assertEqual(result_1, 0)

        result_2 = calculate_number_of_items(6)
        self.assertEqual(result_2, 100)

        result_3 = calculate_number_of_items(12)
        self.assertEqual(result_3, 400)

        result_4 = calculate_number_of_items(25)
        self.assertEqual(result_4, 1170)

        result_5 = calculate_number_of_items(13)
        self.assertEqual(result_5, 570)

    # Testing is rush hour function
    def test_is_rush_hour(self):
        result_1 = is_rush_hour("2024-01-12T16:30:00Z")
        self.assertEqual(result_1, True)

        result_2 = is_rush_hour("2024-01-14T16:30:00Z")
        self.assertEqual(result_2, False)

        result_3 = is_rush_hour("2024-01-12T14:59:59Z")
        self.assertEqual(result_3, False)

        result_4 = is_rush_hour("2024-01-12T15:00:00Z")
        self.assertEqual(result_4, True)

        result_5 = is_rush_hour("2024-01-12T19:00:15Z")
        self.assertEqual(result_5, False)

    # Testing all functions combined
    def test_calculate_delivery_fee(self):
        result_1 = calculate_delivery_fee(790, 2235, 4, "2024-01-15T13:00:00Z")
        self.assertEqual(result_1, 560)

        result_2 = calculate_delivery_fee(790, 2235, 4, "2024-01-12T16:00:00Z")
        self.assertEqual(result_2, 672)

        result_3 = calculate_delivery_fee(1350, 3450, 14, "2024-02-02T17:30:00Z")
        self.assertEqual(result_3, 1284)

        result_4 = calculate_delivery_fee(1350, 3450, 14, "2024-02-03T17:30:00Z")
        self.assertEqual(result_4, 1070)