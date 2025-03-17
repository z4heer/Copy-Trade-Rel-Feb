import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def transformed_tradebook(response):
    try:
        transformed_response = {
            "orders": [
                {
                    "Order_ID": order["ordID"],
                    "Symbol": order["dpName"],
                    "Trading_Symbol": order["trdSym"],
                    "Quantity": int(order["ntQty"]),
                    "Limit_Price": float(order["prc"]),
                    "status": order["sts"],
                    "userid": order["userID"],
                    "Action": order["trsTyp"],
                    "Exchange": order["exc"],
                    "Streaming_Symbol": order["trdSym"],
                    "Duration": "DAY",
                    "Product_Code": order["prdCode"],
                    "Order_Type": "LIMIT",
                    "CurrentQuantity": int(order["ntQty"])
                }
                for order in response["data"]["ord"] if order["sts"] == "complete"
            ]
        }
        return json.dumps(transformed_response, indent=4)
    except Exception as e:
        logger.error(f"Error in transformed_tradebook: {e}")
        raise

def transformed_orderbook(response):
    try:
        transformed_response = {
            "orders": [
                {
                    "Order_ID": order["ordID"],
                    "Symbol": order["dpName"],
                    "Trading_Symbol": order["trdSym"],
                    "Quantity": int(order["ntQty"]),
                    "Limit_Price": float(order["prc"]),
                    "status": order["sts"],
                    "userid": order["userID"],
                    "Action": order["trsTyp"],
                    "Exchange": order["exc"],
                    "Streaming_Symbol": order["trdSym"],
                    "Duration": "DAY",
                    "Product_Code": order["prdCode"],
                    "Order_Type": "LIMIT",
                    "CurrentQuantity": int(order["ntQty"])
        }
                for order in response["data"]["ord"]
            ]
        }
        return json.dumps(transformed_response, indent=4)
    except Exception as e:
        logger.error(f"Error in transformed_orderbook: {e}")
        raise

# Original JSON response
original_response = {
    "appID": "663051cfbac7d699a1c59b96048b50e7",
    "config": {},
    "msgID": "aeae1389-9784-4b23-9774-f0a63f3074d6",
    "srvTm": "string",
    "data": {
        "type": "string",
        "ord": [
            {
                "lstPos": 0,
                "stkPrc": "string",
                "isCOSecLeg": "string",
                "dur": "string",
                "vlDt": "string",
                "rcvTim": "string",
                "rcvEpTim": "string",
                "sym": "string",
                "cpName": "string",
                "exit": "string",
                "syomID": "string",
                "exc": "string",
                "ntQty": "string",
                "dpName": "string",
                "cancel": "string",
                "sipID": "string",
                "nstReqID": "string",
                "ordTyp": "LIMIT",
                "qtyUnits": "string",
                "opTyp": "string",
                "trsTyp": "string",
                "srs": "string",
                "reqQty": "string",
                "prdCode": "CNC",
                "ogt": "string",
                "flQty": "string",
                "trdSym": "string",
                "edit": "string",
                "asTyp": "string",
                "trgPrc": "string",
                "avgPrc": "string",
                "dsQty": "string",
                "ordID": "string",
                "sts": "string",
                "dpInsTyp": "string",
                "rjRsn": "string",
                "userID": "string",
                "dpExpDt": "string",
                "ltSz": "string",
                "tkSz": "string",
                "desc": "string",
                "prc": "string",
                "exONo": "string",
                "exp": "string",
                "rcvDt": "string",
                "pdQty": "string",
                "userCmnt": "string",
                "isSL": False,
                "isTgt": False,
                "flId": "string",
                "rmk": "string",
                "boSeqId": "string",
                "epochTim": "string",
                "ordTim": "string",
                "trgId": "string",
                "dpVal": "string",
                "cta": "string",
                "ltp": "string",
                "vndSrc": "string",
                "bsktOrdId": "string",
                "bsktEpch": "string",
                "brkOrd": [
                    {
                        "flLg": {},
                        "slLg": {},
                        "tgtLg": {}
                    }
                ]
            }
        ]
    }
}



def transformed_ob():
    transformed_response = {
        "orders": [
            {
                "orderid": order["ordID"],
                "symbol": order["sym"],
                "quantity": order["ntQty"],
                "price": order["prc"],
                "status": order["sts"],
                "userid": order["userID"]
            }
            for order in original_response["data"]["ord"]
        ]
    }
    return json.dumps(transformed_response, indent=4)
# Print the transformed JSON response
print(transformed_ob())