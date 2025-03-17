import pandas as pd
import logging

logger = logging.getLogger(__name__)

# Load user data from users.xlsx
try:
    user_data = pd.read_excel('conf/users.xlsx')
    user_data['userid'] = user_data['userid'].astype(str).str.strip()
    user_data['active'] = user_data['active'].astype(bool)
except Exception as e:
    logger.error(f"Error loading user data: {e}")
    raise

def save_user_data():
    """Save the user data back to the Excel file."""
    try:
        user_data.to_excel('conf/users.xlsx', index=False)
    except Exception as e:
        logger.error(f"Error saving user data: {e}")
        raise
def add_user(userid: str, active: bool, reqId: str, username: str, apiKey: str, api_secret_password: str):
    """Add a new user to the user_data DataFrame and save to Excel."""
    global user_data
    new_user = pd.DataFrame([[userid, active, reqId, username, apiKey, api_secret_password]], columns=user_data.columns)
    user_data = pd.concat([user_data, new_user], ignore_index=True)
    save_user_data()
    logger.info(f"User {userid} added successfully.")

def modify_user(userid: str, active: bool = None, reqId: str = None, username: str = None, apiKey: str = None, api_secret_password: str = None):
    """Modify an existing user's data in the user_data DataFrame and save to Excel."""
    global user_data
    if userid not in user_data['userid'].values:
        logger.error(f"User {userid} not found.")
        return

    if active is not None:
        user_data.loc[user_data['userid'] == userid, 'active'] = active
    if reqId is not None:
        user_data.loc[user_data['userid'] == userid, 'reqId'] = reqId
    if username is not None:
        user_data.loc[user_data['userid'] == userid, 'username'] = username
    if apiKey is not None:
        user_data.loc[user_data['userid'] == userid, 'apiKey'] = apiKey
    if api_secret_password is not None:
        user_data.loc[user_data['userid'] == userid, 'api_secret_password'] = api_secret_password

    save_user_data()
    logger.info(f"User {userid} modified successfully.")

def modify_requestid(userid: str, reqId: str = None):
    """Modify an existing user's data in the user_data DataFrame and save to Excel."""
    global user_data
    if userid not in user_data['userid'].values:
        logger.error(f"User {userid} not found.")
        return

    if reqId is not None:
        user_data.loc[user_data['userid'] == userid, 'reqId'] = reqId

    save_user_data()
    logger.info(f"User {userid} modified successfully.")

def modify_status(userid: str, active: str = None):
    """Modify an existing user's data in the user_data DataFrame and save to Excel."""
    global user_data
    if userid not in user_data['userid'].values:
        logger.error(f"User {userid} not found.")
        return

    if active is not None:
        user_data.loc[user_data['userid'] == userid, 'active'] = active

    save_user_data()
    logger.info(f"User {userid} modified successfully.")

def delete_user(userid: str):
    """Delete a user from the user_data DataFrame and save to Excel."""
    global user_data
    if userid not in user_data['userid'].values:
        logger.error(f"User {userid} not found.")
        return

    user_data = user_data[user_data['userid'] != userid]
    save_user_data()
    logger.info(f"User {userid} deleted successfully.")