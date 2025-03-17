from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

# Mock user data
mock_users = [
    {"userid": "user1", "username": "username1", "active": True, "apiKey": "abc", "api_secret_password": "cds",
     "reqId": "ddd"},
    {"userid": "user2", "username": "username2", "active": True, "apiKey": "aaa", "api_secret_password": "bbb",
     "reqId": "ccc"},
    {"userid": "user3", "username": "username3", "active": False, "apiKey": "aa", "api_secret_password": "bb",
     "reqId": "cc"},
    {"userid": "user4", "username": "username4", "active": True, "apiKey": "cc", "api_secret_password": "dd",
     "reqId": "aa"}
]

# Mock responses
mock_trade_response = {
    "status": "success",
    "message": "Trade executed successfully"
}

mock_position_square_off_response = {
    "status": "success",
    "message": "Position squared off successfully"
}

mock_modify_trade_response = {
    "status": "success",
    "message": "Trade modified successfully"
}

mock_cancel_trade_response = {
    "status": "success",
    "message": "Trade cancelled successfully"
}

mock_order_book_response = {
    "orders": [
        {"orderid": "order1", "symbol": "AAPL", "quantity": 50, "price": 150, "status": "Filled", "userid": "user1"},
        {"orderid": "order2", "symbol": "GOOG", "quantity": 10, "price": 2000, "status": "Pending", "userid": "user2"}
    ]
}

mock_net_position_response = {
    "positions": [
        {"symbol": "AAPL", "quantity": 100, "average_price": 145, "userid": "user1","order_id": "order1"},
        {"symbol": "GOOG", "quantity": 20, "average_price": 1950, "userid": "user2","order_id": "order2"}
    ]
}

mock_holdings_response = {
    "holdings": [
        {"symbol": "AAPL", "quantity": 100, "current_price": 148, "userid": "user1","order_id": "order1"},
        {"symbol": "GOOG", "quantity": 20, "current_price": 2020, "userid": "user2","order_id": "order2"}
    ]
}

@app.route('/api/order_details', methods=['POST'])
def order_details():
    return jsonify(mock_modify_trade_response)


@app.route('/api/users', methods=['GET'])
def get_mock_users():
    active_users = [user for user in mock_users if user['active']]
    return jsonify(active_users)

@app.route('/api/place_trade', methods=['POST'])
def place_mock_trade():
    trade_data = request.json
    return jsonify(mock_trade_response)

@app.route('/api/position_square_off', methods=['POST'])
def position_mock_square_off():
    trade_data = request.json
    return jsonify(mock_position_square_off_response)

@app.route('/api/modify_trade/<userID>', methods=['PUT'])
def modify_mock_trade(userID):
    trade_data = request.json
    return jsonify(mock_modify_trade_response)

@app.route('/api/cancel_trade', methods=['POST'])
def cancel_mock_trade():
    trade_data = request.json
    return jsonify(mock_cancel_trade_response)

@app.route('/api/order_book', methods=['POST'])
def order_mock_book():
    return jsonify(mock_order_book_response)

@app.route('/api/net_position', methods=['POST'])
def net_mock_position():
    return jsonify(mock_net_position_response)

@app.route('/api/holdings', methods=['POST'])
def mock_holdings():
    return jsonify(mock_holdings_response)

@app.route('/api/accounts/loginvendor', methods=['POST'])
def login_vendor():
    data = request.json
    userid = data.get('userid')
    password = data.get('pwd')
    if "copy" == userid or "trade" == password:
        return jsonify({"status": "success", "message": f"User {userid} logged in successfully"})
    return jsonify({"status": "error", "message": "Invalid credentials or inactive user"}), 401

if __name__ == '__main__':
    app.run(port=5001, debug=True)