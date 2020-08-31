import unittest
import random

def computeShipments(orders: dict, warehouses: list) -> list:
    '''

    :param orders: A map of items that are ordered and their values
    :param warehouses: A list of objects that has a warehouse name and its inventory distribution
    :return: A list of warehouses that will produce the cheapest shipment
    '''
    min_shipments = []
    for warehouse in warehouses:
        curr_warehouse = dict()
        curr_warehouse[warehouse["name"]] = {}
        for item_name, item_value in warehouse["inventory"].items():
            if item_name in orders:
                if orders[item_name] == item_value:
                    remainder = item_value
                elif orders[item_name] > item_value:
                    remainder = item_value
                else:
                    remainder = orders[item_name]
                orders[item_name] -= item_value
                curr_warehouse[warehouse["name"]][item_name] = remainder
                if orders[item_name] <= 0:
                    del orders[item_name]
                if len(orders) == 0:
                    min_shipments.append(curr_warehouse)
                    return min_shipments
        min_shipments.append(curr_warehouse)
    return []


class TestComputeShipments(unittest.TestCase):
    def test_one_warehouse_1(self):
        test = computeShipments({"apple": 1}, [{"name": "owd", "inventory": {"apple": 1}}])
        self.assertCountEqual(test, [{"owd": {"apple": 1}}])

    def test_multiple_warehouse_1(self):
        test = computeShipments({"apple": 10},
                                [{"name": "owd", "inventory": {"apple": 5}}, {"name": "dm", "inventory": {"apple": 5}}])
        self.assertCountEqual(test, [{"dm": {"apple": 5}}, {"owd": {"apple": 5}}])

    def test_not_enough_inventory_1(self):
        test = computeShipments({"apple": 1}, [{"name": "owd", "inventory": {"apple": 0}}])
        self.assertCountEqual(test, [])

    def test_not_enough_inventory_2(self):
        test = computeShipments({"apple": 2}, [{"name": "owd", "inventory": {"apple": 1}}])
        self.assertCountEqual(test, [])

    def test_multiple_warehouse_2(self):
        orders = {"apple": random.randint(1,10),
                  "banana": random.randint(1,10),
                  "orange": random.randint(1,10)}
        comparable = orders.copy()
        warehouses = [{"name": "a", "inventory": {"apple" : random.randint(0,10), "banana" : random.randint(0,10),
                                                  "orange" : random.randint(0,10)}},
                      {"name": "b", "inventory": {"apple": random.randint(0, 10), "banana": random.randint(0, 10),
                                                  "orange": random.randint(0, 10)}},
                      {"name": "c", "inventory": {"apple": random.randint(0, 10), "banana": random.randint(0, 10),
                                                  "orange": random.randint(0, 10)}},
                      {"name": "d", "inventory": {"apple": random.randint(0, 10), "banana": random.randint(0, 10),
                                                  "orange": random.randint(0, 10)}}
                      ]
        test = computeShipments(orders, warehouses)
        output_dict = {"apple" : 0, "banana": 0, "orange" : 0}
        for output in test:
            for v in output.values():
                for j,k in v.items():
                    output_dict[j] += k
        self.assertDictEqual(output_dict, comparable)