import json

from flask import Flask, request, jsonify, Response
from api_connect_wrapper import APIConnectWrapper
import pandas as pd
import logging
from flask_cors import CORS
from transform import transformed_orderbook, transformed_tradebook
from users import add_user, modify_user, delete_user, modify_status, load_user_data, save_user_data, get_user_info, \
    get_user_info_1, load_all_user_data

app = Flask(__name__)
CORS(app)  # Enable CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load user data from users.xlsx
user_data = load_user_data()

def get_active_users(user_data):
    # Ensure 'active' and 'session_active' columns are boolean type
    user_data['active'] = user_data['active'].astype(bool)
    user_data['session_active'] = user_data['session_active'].astype(bool)
    return user_data[user_data['active'] & user_data['session_active']]

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        active_users = get_active_users(user_data).to_dict(orient='records')
        return jsonify(active_users)
    except Exception as e:
        logger.error(f"Error in get_users: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/accounts/loginvendor', methods=['POST'])
def login_vendor():
    data = request.json
    userid = data.get('userid')
    password = data.get('pwd')
    if "copy" == userid or "trading" == password:
            return jsonify({"success": True ,"status": "success", "message": f"User {userid} logged in successfully"})
    return jsonify({"success": False, "status": "error", "message": "Invalid credentials or inactive user"}), 401

@app.route('/api/accounts/logindata', methods=['POST'])
def login_data():
    try:
        userid = request.json.get('userid')
        if not userid:
            raise ValueError("Missing userid")

        user_info = get_user_info(user_data, userid)
        if user_info is None:
            return jsonify({"error": "User not found or not active"}), 404

        api_connect = APIConnectWrapper(user_info)
        response = api_connect.get_login_data()
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in login_data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/place_trade', methods=['POST'])
def place_trade():
    try:
        trade_data = request.json
        if not trade_data:
            raise ValueError("Missing trade data")
        if 'symbol' in trade_data:
            del trade_data['symbol']
        active_users = get_active_users(user_data)
        responses = []
        for _, user_info in active_users.iterrows():
            trade_data = APIConnectWrapper.validate_and_convert_trade_data(trade_data)
            api_connect = APIConnectWrapper(user_info)
            response = api_connect.place_trade(trade_data)
            responses.append(response)
        return jsonify(responses)
    except Exception as e:
        logger.error(f"Error in place_trade: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/modify_trade/<userID>', methods=['PUT'])
def modify_trade(userID):
    try:
        userid = request.json.get('userid')
        if not userid:
            raise ValueError("Missing userid")

        user_info = get_user_info(user_data, userid)
        if user_info is None:
            return jsonify({"error": "User not found or not active"}), 404

        trade_data = request.json
        logger.info(f"trade_data= {trade_data}")
        if not trade_data:
            raise ValueError("Missing trade data")
        if 'userid' in trade_data:
            del trade_data['userid']
        if 'symbol' in trade_data:
            del trade_data['symbol']

        trade_data = APIConnectWrapper.validate_and_convert_trade_data(trade_data)

        api_connect = APIConnectWrapper(user_info)
        response = api_connect.modify_trade(userID, trade_data)
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in modify_trade: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/cancel_trade', methods=['POST'])
def cancel_trade():
    try:
        userid = request.json.get('userid')
        if not userid:
            raise ValueError("Missing userid")

        user_info = get_user_info(user_data, userid)
        if user_info is None:
            return jsonify({"error": "User not found or not active"}), 404

        trade_data = request.json
        if not trade_data:
            raise ValueError("Missing trade data")

        trade_data = APIConnectWrapper.validate_and_convert_trade_data(trade_data)

        api_connect = APIConnectWrapper(user_info)
        if 'userid' in trade_data:
            del trade_data['userid']
        response = api_connect.cancel_trade(trade_data)
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in cancel_trade: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/position_square_off_all', methods=['POST'])
def position_square_off():
    try:
        trade_data = request.json
        if 'userid' not in trade_data:
            raise ValueError("Missing userid")
        if not trade_data:
            raise ValueError("Missing trade data")

        active_users = get_active_users(user_data)
        responses = []
        for _, user_info in active_users.iterrows():
            if 'userid' in trade_data:
                del trade_data['userid']
            #logger.debug(f"before validate_and_convert_trade_data()= {trade_data}")
            trade_data = APIConnectWrapper.validate_and_convert_trade_data(trade_data)
            api_connect = APIConnectWrapper(user_info)
            #logger.debug(f"after position_square_off()= {trade_data}")
            response = api_connect.position_square_off(trade_data)
            #logger.debug(f"after position_square_off() -response= {response}")
            responses.append(response)
        return jsonify(responses)
    except Exception as e:
        logger.error(f"Error in position_square_off: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/position_square_off', methods=['POST'])
def position_square_off_user_specific():
    try:
        trade_data = request.json
        userid = request.json.get('userid')
        if 'userid' not in trade_data:
            raise ValueError("Missing userid")
        if not trade_data:
            raise ValueError("Missing trade data")

        trade_data = APIConnectWrapper.validate_and_convert_trade_data(trade_data)
        user_info = get_user_info(user_data, userid)
        api_connect = APIConnectWrapper(user_info)
        response = api_connect.position_square_off(trade_data)
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in position_square_off: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/order_book', methods=['POST'])
def order_book():
    try:
        userid = request.json.get('userid')
        if not userid:
            raise ValueError("Missing userid")

        user_info = get_user_info(user_data, userid)
        if user_info is None:
            return jsonify({"error": "User not found or not active"}), 404

        api_connect = APIConnectWrapper(user_info)
        response = api_connect.order_book()
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in order_book: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders', methods=['POST'])
def orders():
    try:
        active_users = get_active_users(user_data)
        all_orders = []
        for _, user_info in active_users.iterrows():
            api_connect = APIConnectWrapper(user_info)
            response = api_connect.order_book()
            if "eq" in response:
                response = response["eq"]
                if "data" in response and "ord" in response["data"]:
                    all_orders.extend(response["data"]["ord"])
                else:
                    return jsonify({"error": "Invalid response structure / No Data Found"}), 500
            else:
                return jsonify({"error": "Invalid response structure"}), 500
        consolidated_response = {"data": {"ord": all_orders}}
        response_data = transformed_orderbook(consolidated_response)
        return jsonify(response_data), 200
    except Exception as e:
        logger.error(f"Error in orders: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/trades', methods=['POST'])
def trades():
    try:
        active_users = get_active_users(user_data)
        all_orders = []
        for _, user_info in active_users.iterrows():
            api_connect = APIConnectWrapper(user_info)
            response = api_connect.order_book()
            if "eq" in response:
                response = response["eq"]
                if "data" in response and "ord" in response["data"]:
                    all_orders.extend(response["data"]["ord"])
                else:
                    return jsonify({"error": "Invalid response structure / No Data Found"}), 500
            else:
                return jsonify({"error": "Invalid response structure"}), 500
        consolidated_response = {"data": {"ord": all_orders}}
        response_data = transformed_tradebook(consolidated_response)
        return jsonify(response_data), 200
    except Exception as e:
        logger.error(f"Error in trades(): {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/order_details', methods=['POST'])
def order_details():
    try:
        userid = request.json.get('userid')
        if not userid:
            raise ValueError("Missing userid")

        user_info = get_user_info(user_data, userid)
        if user_info is None:
            return jsonify({"error": "User not found or not active"}), 404

        trade_data = request.json
        order_id = request.json.get('order_id')
        if not order_id:
            raise ValueError("Missing order_id")

        trade_data = APIConnectWrapper.validate_and_convert_trade_data(trade_data)

        exchange = trade_data.get('Exchange')
        if not exchange:
            raise ValueError("Missing exchange")

        api_connect = APIConnectWrapper(user_info)
        response = api_connect.order_details(order_id, exchange)
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in order_details: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/holdings', methods=['POST'])
def holdings():
    try:
        userid = request.json.get('userid')
        if not userid:
            raise ValueError("Missing userid")

        user_info = get_user_info(user_data, userid)
        if user_info is None:
            return jsonify({"error": "User not found or not active"}), 404

        api_connect = APIConnectWrapper(user_info)
        response = api_connect.holdings()
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in holdings: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/holdings_all_users', methods=['POST'])
def holdings_all_users():
    try:
        active_users = get_active_users(user_data)
        all_holdings = []

        for _, user_info in active_users.iterrows():
            userid = user_info['userid']
            api_connect = APIConnectWrapper(user_info)
            response = api_connect.holdings()

            if isinstance(response, str):
                response = json.loads(response)
                logger.debug(f"isinstance- {response}")

            if "eq" in response and "data" in response["eq"] and "rmsHdg" in response["eq"]["data"]:
                holdings = response["eq"]["data"]["rmsHdg"]
                mapped_holdings = [
                    {
                        "userid": userid,
                        "Symbol": holding.get("dpName", ""),
                        "TradingSymbol": holding.get("trdSym", ""),
                        "Exchange": holding.get("exc", "NSE"),
                        "BuyQuantity": holding.get("totalQty", 0),
                        "BuyPrice": 0,
                        "TotalVal": holding.get("totalVal", ""),
                        "Ltp": holding.get("ltp", ""),
                        "ChangePcToday": holding.get("chgP", ""),
                        "ProductCode": "CNC" if "cncRmsHdg" in holding else "NORMAL",
                        "StreamingSymbol": holding.get("trdSym", "")
                    }
                    for holding in holdings
                ]
                all_holdings.extend(mapped_holdings)
            else:
                logger.error(f"Response for userid {userid} does not contain required keys")
                return jsonify({"error": "Invalid response structure / No Data Found"}), 500
        #logger.debug(f"all holdings= {all_holdings}")
        formatted_response = {
            "Holdings": all_holdings
        }

        return jsonify(formatted_response), 200
    except Exception as e:
        logger.error(f"Error in holdings_all_users: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/net_position', methods=['POST'])
def net_position():
    try:
        userid = request.json.get('userid')
        if not userid:
            raise ValueError("Missing userid")

        user_info = get_user_info(user_data, userid)
        if user_info is None:
            return jsonify({"error": "User not found or not active"}), 404

        api_connect = APIConnectWrapper(user_info)
        response = api_connect.net_position()
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in net_position: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/net_position_f', methods=['POST'])
def net_position_formatted():
    try:
        data = request.get_json()
        logger.debug(f"Request JSON: {data}")
        userid = data.get('userid')
        if not userid:
            raise ValueError("Missing userid")

        user_info = get_user_info(user_data, userid)
        if user_info is None:
            return jsonify({"error": "User not found or not active"}), 404

        api_connect = APIConnectWrapper(user_info)
        response = api_connect.net_position()
        response = json.loads(response)
        positions = response.get("eq", {}).get("data", {}).get("pos", [])
        mapped_positions = [
            {
                "userid":userid,
                "Symbol": pos.get("dpName", ""),
                "TradingSymbol": pos.get("trdSym", ""),
                "Exchange": pos.get("exc", ""),
                "BuyQuantity": pos.get("ntByQty", 0),
                "SellQuantity": pos.get("ntSlQty", 0),
                "BuyPrice": pos.get("avgByPrc", ""),
                "SellPrice": pos.get("avgSlPrc", ""),
                "ProductCode": pos.get("prdCode", ""),
                "StreamingSymbol": pos.get("trdSym", ""),
                "squareOffSts": pos.get("sqOff", "false")
            }
            for pos in positions
        ]

        formatted_response = {
            "Positions": mapped_positions
        }

        return jsonify(formatted_response), 200
    except Exception as e:
        logger.error(f"Error in net_position: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/net_position_all_users', methods=['POST'])
def net_position_all_users():
    try:
        active_users = get_active_users(user_data)
        all_positions = []

        for _, user_info in active_users.iterrows():
            userid = user_info['userid']
            api_connect = APIConnectWrapper(user_info)
            response = api_connect.net_position()
            response = json.loads(response)
            if "eq" in response and "data" in response["eq"] and "pos" in response["eq"]["data"]:
                positions = response["eq"]["data"]["pos"]
                logger.debug(f"positions for userid {userid}: {positions}")

                mapped_positions = [
                    {
                        "userid": userid,
                        "Symbol": pos.get("dpName", ""),
                        "TradingSymbol": pos.get("trdSym", ""),
                        "Exchange": pos.get("exc", ""),
                        "BuyQuantity": pos.get("ntByQty", 0),
                        "SellQuantity": pos.get("ntSlQty", 0),
                        "BuyPrice": pos.get("avgByPrc", ""),
                        "SellPrice": pos.get("avgSlPrc", ""),
                        "ProductCode": pos.get("prdCode", ""),
                        "StreamingSymbol": pos.get("trdSym", ""),
                        "squareOffSts": pos.get("sqOff", "false")
                    }
                    for pos in positions
                ]
                all_positions.extend(mapped_positions)
            else:
                logger.error(f"Response for userid {userid} does not contain required keys")
                return jsonify({"error": "Invalid response structure / No Data Found!"}), 500

        formatted_response = {
            "Positions": all_positions
        }

        return jsonify(formatted_response), 200
    except Exception as e:
        logger.error(f"Error in net_position_all_users: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/all_users', methods=['GET'])
def get_all_users():
    try:
        users = load_all_user_data().to_dict(orient='records')
        return jsonify(users)
    except Exception as e:
        logger.error(f"Error in get_users: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/isin", methods=["GET"])
def get_isin():
    symbol = request.args.get("symbol")
    logger.info(f"Symbol= {symbol}")
    if not symbol:
        return jsonify({"error": "Symbol is required"}), 400

    isin, error = get_isin_from_csv(symbol)
    if error:
        return jsonify({"error": error}), 404

    return jsonify({"isin": isin})

@app.route('/api/add_user', methods=['POST'])
def api_add_user():
    global user_data
    try:
        data = request.get_json()
        userid = data.get('userid')
        active = data.get('active')
        reqId = data.get('reqId')
        username = data.get('username')
        apikey = data.get('apiKey')
        apisec = data.get('api_secret_password')

        if not userid or active is None or not reqId or not username:
            logger.debug("error: Missing required fields")
            return jsonify({"error": "Missing required fields"}), 400

        # Check if the userid already exists
        if userid in user_data['userid'].values:
            logger.debug("error: User with this userid already exists")
            return jsonify({"error": "User with this userid already exists"}), 400

        user_data = add_user(user_data, userid, active, reqId, username, apikey, apisec)
        logger.debug("success: User added successfully")
        return jsonify({"message": "User added successfully"}), 200
    except Exception as e:
        logger.error(f"Error in api_add_user: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/modify_user', methods=['POST'])
def api_modify_user():
    global user_data
    try:
        data = request.get_json()
        userid = data.get('userid')
        logger.debug(f"Modify_user()- {data}")
        if not userid:
            return jsonify({"error": "Missing userid"}), 400

        active = data.get('active')
        reqId = data.get('reqId')
        username = data.get('username')
        apikey = data.get('apiKey')
        apisec = data.get('api_secret_password')

        user_data = modify_user(user_data, userid, active, reqId, username, apikey, apisec,False)
        return jsonify({"message": "User modified successfully"}), 200
    except Exception as e:
        logger.error(f"Error in api_modify_user: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/validate_user', methods=['POST'])
def validate():
    global user_data
    try:
        userid = request.json.get('userid')
        logger.info(f"validate()- userid= {userid}")
        if not userid:
            raise ValueError("Missing userid")

        user_info = get_user_info_1(user_data, userid)
        logger.info(f"user_info= {user_info}")
        if user_info is None:
            return jsonify({"error": "User not found or not active"}), 404
        user_data = modify_status(user_data, userid, session_active=False)
        api_connect = APIConnectWrapper(user_info)
        user_data = modify_status(user_data, userid, session_active=True)
        return jsonify({"success": "User login and RequestId Validation completed"})
    except Exception as e:
        logger.error(f"Error in login_data: {e}, Please make sure userid and fresh requestid are correct")
        return jsonify({"error": str(e), "message": "Please make sure userid and fresh requestid are correct"}), 500

@app.route('/api/delete_user', methods=['POST'])
def api_delete_user():
    global user_data
    try:
        data = request.get_json()
        userid = data.get('userid')

        if not userid:
            return jsonify({"error": "Missing userid"}), 400

        user_data = delete_user(user_data, userid)
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        logger.error(f"Error in api_delete_user: {e}")
        return jsonify({"error": str(e)}), 500

def get_isin_from_csv(symbol):
    try:
        df = pd.read_csv("conf/EQUITY_L.csv")
    except FileNotFoundError:
        return None, "CSV file not found. Please download it manually."
    df.columns = df.columns.str.upper()
    stock_data = df[df["SYMBOL"] == symbol.upper()]

    if stock_data.empty:
        return None, f"Symbol {symbol} not found in Bhavcopy"
    logger.info(f"stock_data= {stock_data}")
    isin = stock_data["ISIN NUMBER"].values[0].strip()
    return isin, None

if __name__ == '__main__':
    app.run(debug=True)