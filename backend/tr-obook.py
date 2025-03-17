from flask import Flask, jsonify
import json
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_active_users():
    # Dummy function to simulate getting active users
    import pandas as pd
    data = {
        'userid': [1, 2],
        'username': ['user1', 'user2'],
        'api_key': ['key1', 'key2'],
        'api_secret': ['secret1', 'secret2']
    }
    return pd.DataFrame(data)

class APIConnectWrapper:
    def __init__(self, user_info):
        self.user_info = user_info

    def order_book(self):
        # Dummy function to simulate an API call
        response = {
            "eq": {
                'appID': 'a5cbb543e3a7fb6bb063356377d6ad55',
                'config': {'app': 1, 'exp': 1741651223046, 'info': 4},
                'data': {
                    'type': 'orderBookResponse',
                    'ord': [
                        {
                            'ordID': '250311000114251',
                            'dpName': 'UJJIVANSFB',
                            'ntQty': '1',
                            'prc': '34.05',
                            'sts': 'open',
                            'userID': '45937331'
                        },
                        {
                            'ordID': '250311000108993',
                            'dpName': 'UJJIVANSFB',
                            'ntQty': '1',
                            'prc': '34.20',
                            'sts': 'open',
                            'userID': '45937331'
                        }
                    ]
                },
                'msgID': 'e72d4ce2-f01a-43b2-9079-b70b2a83e46f',
                'srvTm': 1741677771367
            },
            "comm": ""
        }
        return response

@app.route('/apis/orders', methods=['POST'])
def orders():
    try:
        active_users = get_active_users()
        all_orders = []
        for _, user_info in active_users.iterrows():
            api_connect = APIConnectWrapper(user_info)
            response = api_connect.order_book()
            logger.debug(f"Received response: {response}")
            if "eq" in response:
                response = response["eq"]
                logger.debug(f"Extracted 'eq' response: {response}")
                all_orders.extend(response["data"]["ord"])
            else:
                logger.error("Response does not contain 'eq' key")
                return jsonify({"error": "Invalid response structure"}), 500
        consolidated_response = {"data": {"ord": all_orders}}
        return transformed_orderbook(consolidated_response)
    except Exception as e:
        logger.error(f"Error in order_book: {e}")
        return jsonify({"error": str(e)}), 500

def transformed_orderbook(response):
    try:
        transformed_response = {
            "orders": [
                {
                    "orderid": order["ordID"],
                    "symbol": order["dpName"],
                    "quantity": order["ntQty"],
                    "price": order["prc"],
                    "status": order["sts"],
                    "userid": order["userID"]
                }
                for order in response["data"]["ord"]
            ]
        }
        return json.dumps(transformed_response, indent=4)
    except Exception as e:
        logger.error(f"Error in transformed_orderbook: {e}")
        raise

if __name__ == '__main__':
    app.run(debug=True)
