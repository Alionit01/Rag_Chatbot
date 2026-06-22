import json
import os
from config import ORDERS_FILE


def load_orders():
    """
    Safely loads order entries from the json file database.
    """
    if not os.path.exists(ORDERS_FILE):
        return {}

    try:
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

            # If the file was saved as a list, convert it to a working dictionary map
            if isinstance(data, list):
                return {str(item.get("order_id")): item for item in data if isinstance(item, dict)}

            return data
    except (FileNotFoundError, json.JSONDecodeError):
        # Return a fresh dictionary if file is empty or broken
        return {}


def save_orders(order_data):
    """
    Updates or inserts an order validation state into disk file storage.
    """
    # 1. Load current database map state safely
    orders = load_orders()

    # 2. Extract key ID string and map it to save the fresh record payload
    order_id = str(order_data["order_id"])
    orders[order_id] = order_data

    # 3. Write back changes safely onto the disk file
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, indent=4)