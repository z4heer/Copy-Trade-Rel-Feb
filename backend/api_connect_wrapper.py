import json

from APIConnect.APIConnect import APIConnect
from APIConnect.order import Order
from constants.exchange import ExchangeEnum
from constants.order_type import OrderTypeEnum
from constants.product_code import ProductCodeENum
from constants.duration import DurationEnum
from constants.action import ActionEnum
import logging

logger = logging.getLogger(__name__)

class APIConnectWrapper:
    def __init__(self, user_info):
        try:
            self.api_connect = APIConnect(
                user_info['apiKey'],
                user_info['api_secret_password'],
                user_info['reqId'],
                False,
                'conf/settings.ini'
            )
        except Exception as e:
            logger.error(f"Error initializing APIConnect: {e}")
            raise

    def login_vendor(self, vendorID, pwd):
        try:
            return self.api_connect.Post(f'/accounts/loginvendor/{vendorID}', json={'pwd': pwd})
        except Exception as e:
            logger.error(f"Error in login_vendor: {e}")
            raise

    def get_login_data(self):
        try:
            return self.api_connect.GetLoginData()
        except Exception as e:
            logger.error(f"Error in get_login_data: {e}")
            raise

    def place_trade(self, trade_data):
        try:
            return self.api_connect.PlaceTrade(**trade_data)
        except Exception as e:
            logger.error(f"Error in place_trade: {e}")
            raise

    def modify_trade(self, userID, trade_data):
        try:
            return self.api_connect.ModifyTrade(**trade_data)
        except Exception as e:
            logger.error(f"Error in modify_trade: {e}")
            raise

    def cancel_trade(self, trade_data):
        try:
            return self.api_connect.CancelTrade(**trade_data)
        except Exception as e:
            logger.error(f"Error in cancel_trade: {e}")
            raise

    def position_square_off(self, trade_data):
        try:
            # Convert each order in sqrLst to Order object after validating and converting enums
            order_list = [Order(**self.validate_and_convert_trade_data(order)) for order in trade_data['sqrLst']]
            return self.api_connect.PositionSquareOff(orderlist=order_list)
        except Exception as e:
            logger.error(f"Error in position_square_off: {e}")
            raise

    def order_book(self):
        try:
            response = self.api_connect.OrderBook()
            if isinstance(response, str):
                response = json.loads(response)
            return response
        except Exception as e:
            logger.error(f"Error in order_book: {e}")
            raise

    def order_details(self, order_id, exchange):
        try:
            return self.api_connect.OrderDetails(OrderId=order_id, Exchange=exchange)
        except Exception as e:
            logger.error(f"Error in order_details: {e}")
            raise

    def holdings(self):
        try:
            response = self.api_connect.Holdings()
            if isinstance(response, str):
                response = json.loads(response)
            return response
        except Exception as e:
            logger.error(f"Error in holdings: {e}")
            raise

    def net_position(self):
        try:
            return self.api_connect.NetPosition()
        except Exception as e:
            logger.error(f"Error in net_position: {e}")
            raise

    @staticmethod
    def validate_and_convert_trade_data(trade_data):
        try:
            if 'Exchange' in trade_data:
                trade_data['Exchange'] = ExchangeEnum[trade_data['Exchange'].upper()]
            if 'Action' in trade_data:
                trade_data['Action'] = ActionEnum[trade_data['Action'].upper()]
            if 'Order_Type' in trade_data:
                trade_data['Order_Type'] = OrderTypeEnum[trade_data['Order_Type'].upper()]
            if 'Product_Code' in trade_data:
                trade_data['Product_Code'] = ProductCodeENum[trade_data['Product_Code'].upper()]
            if 'ProductCode' in trade_data:
                trade_data['ProductCode'] = ProductCodeENum[trade_data['ProductCode'].upper()]
            if 'OrderType' in trade_data:
                trade_data['OrderType'] = OrderTypeEnum[trade_data['OrderType'].upper()]
            if 'Duration' in trade_data:
                trade_data['Duration'] = DurationEnum[trade_data['Duration'].upper()]
            return trade_data
        except KeyError as e:
            logger.error(f"Invalid enum value: {e}")
            raise ValueError(f"Invalid enum value: {e}")
        except Exception as e:
            logger.error(f"Error in validate_and_convert_trade_data: {e}")
            raise