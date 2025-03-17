from flask import Flask, request, jsonify
from api_connect_wrapper import APIConnectWrapper
import pandas as pd
import logging
import json
from transform import transformed_orderbook

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load user data from users.xlsx
try:
    user_data = pd.read_excel('conf/users.xlsx')
    user_data['userid'] = user_data['userid'].astype(str).str.strip()
    user_data['active'] = user_data['active'].astype(bool)
except Exception as e:
    logger.error(f"Error loading user data: {e}")
    raise

def get_user_info(userid):
    userid = str(userid).strip()
    user_info = user_data[user_data['userid'] == userid]
    if not user_info.empty and user_info['active'].iloc[0]:
        return user_info.iloc[0]
    return None

def get_active_users():
    return user_data[user_data['active']]

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        active_users = get_active_users()
        return jsonify(active_users)
    except Exception as e:
        logger.error(f"Error in get_users: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/dashboard', methods=['GET'])
def dashboard():
    try:
        active_users = get_active_users()
        return jsonify(active_users)
    except Exception as e:
        logger.error(f"Error in dashboard: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/place_trade', methods=['POST'])
def place_trade():
    try:
        data = request.json
        trade_data = data.get('trade_data')
        if not trade_data:
            raise ValueError("Missing trade data")

        active_users = get_active_users()
        responses = []
        for _, user_info in active_users.iterrows():
            api_connect = APIConnectWrapper(user_info)
            response = api_connect.place_trade(trade_data)
            responses.append(response)
        return jsonify(responses)
    except Exception as e:
        logger.error(f"Error in place_trade: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/order_book', methods=['POST'])
def order_book():
    try:
        active_users = get_active_users()
        all_responses = []
        for _, user_info in active_users.iterrows():
            api_connect = APIConnectWrapper(user_info)
            response = api_connect.order_book()
            #logger.debug(f"order_book()- Received response: {response}")
            if "eq" in response:
                response = response["eq"]
                #logger.debug(f"Extracted 'eq' response: {response}")
            else:
                #logger.error("Response does not contain 'eq' key")
                return jsonify({"error": "Invalid response structure"}), 500
            all_responses.append(response)
            all_responses.append(response)
        # Combine all responses if necessary, for simplicity assuming one response here
        return transformed_orderbook(response)
    except Exception as e:
        logger.error(f"Error in order_book: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/modify_order/<userid>/<orderid>', methods=['PUT'])
def modify_order(userid, orderid):
    try:
        trade_data = request.json
        if not trade_data:
            raise ValueError("Missing trade data")

        user_info = get_user_info(userid)
        if user_info is None:
            return jsonify({"error": "User not found or not active"}), 404

        api_connect = APIConnectWrapper(user_info)
        response = api_connect.modify_trade(orderid, trade_data)
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in modify_order: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/cancel_order/<userid>/<orderid>', methods=['POST'])
def cancel_order(userid, orderid):
    try:
        trade_data = request.json
        if not trade_data:
            raise ValueError("Missing trade data")

        user_info = get_user_info(userid)
        if user_info is None:
            return jsonify({"error": "User not found or not active"}), 404

        api_connect = APIConnectWrapper(user_info)
        response = api_connect.cancel_trade(orderid, trade_data)
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in cancel_order: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/net_position', methods=['POST'])
def net_position():
    try:
        active_users = get_active_users()
        positions = []
        for _, user_info in active_users.iterrows():
            api_connect = APIConnectWrapper(user_info)
            response = api_connect.net_position()
            for position in response.get('positions', []):
                position['userid'] = user_info['userid']
                positions.append(position)
        return jsonify({"positions": positions})
    except Exception as e:
        logger.error(f"Error in net_position: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/holdings', methods=['POST'])
def holdings():
    try:
        active_users = get_active_users()
        holdings = []
        for _, user_info in active_users.iterrows():
            api_connect = APIConnectWrapper(user_info)
            response = api_connect.holdings()
            for holding in response.get('holdings', []):
                holding['userid'] = user_info['userid']
                holdings.append(holding)
        return jsonify({"holdings": holdings})
    except Exception as e:
        logger.error(f"Error in holdings: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/position_square_off/<userid>/<orderid>', methods=['POST'])
def position_square_off(userid, orderid):
    try:
        trade_data = request.json
        if not trade_data:
            raise ValueError("Missing trade data")

        user_info = get_user_info(userid)
        if user_info is None:
            return jsonify({"error": "User not found or not active"}), 404

        api_connect = APIConnectWrapper(user_info)
        response = api_connect.position_square_off(orderid, trade_data)
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in position_square_off: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)