import os
from utils import resource_path
import pandas as pd
import logging

logger = logging.getLogger(__name__)
xls_path = resource_path("conf/users.xlsx")
print("Looking for:", xls_path)
print("Exists?", os.path.exists(xls_path))
def load_user_data():
    """Load user data from the Excel file."""
    try:
        user_data = pd.read_excel(xls_path)
        #user_data = pd.read_excel('conf/users.xlsx')
        user_data['userid'] = user_data['userid'].astype(str).str.strip()
        user_data['active'] = user_data['active'].astype(bool)
        return user_data
    except Exception as e:
        logger.error(f"Error loading user data: {e}")
        raise

def load_all_user_data():
    """Load user data from the Excel file."""
    try:
        user_data = pd.read_excel(xls_path)
        #user_data = pd.read_excel('conf/users.xlsx')
        user_data['userid'] = user_data['userid'].astype(str).str.strip()
        return user_data
    except Exception as e:
        logger.error(f"Error loading user data: {e}")
        raise

def save_user_data(user_data):
    """Save the user data back to the Excel file."""
    try:
        user_data.to_excel(xls_path, index=False)
    except Exception as e:
        logger.error(f"Error saving user data: {e}")
        raise

def add_user(user_data, userid: str, active: bool, reqId: str, username: str, apiKey: str, api_secret_password: str):
    """Add a new user to the user_data DataFrame and save to Excel."""
    new_user = pd.DataFrame([[apiKey, api_secret_password, reqId, userid, username, bool(active), False]], columns=user_data.columns)
    user_data = pd.concat([user_data, new_user], ignore_index=True)
    save_user_data(user_data)
    logger.info(f"User {userid} added successfully.")
    return user_data

def modify_user(user_data, userid: str, active: bool = None, reqId: str = None, username: str = None
                , apiKey: str = None, api_secret_password: str = None, session_active: bool = None):
    """Modify an existing user's data in the user_data DataFrame and save to Excel."""
    if userid not in user_data['userid'].values:
        raise ValueError(f"User {userid} not found.")

    modifications = {
        'active': active,
        'reqId': reqId,
        'username': username,
        'apiKey': apiKey,
        'api_secret_password': api_secret_password,
        'session_active' : session_active
    }
    for field, value in modifications.items():
        if value is not None:
            if field == 'active' or field == session_active:
                user_data.loc[user_data['userid'] == userid, field] = bool(value)
            else:
                user_data.loc[user_data['userid'] == userid, field] = value
            user_data.loc[user_data['userid'] == userid, field] = value
    save_user_data(user_data)
    logger.info(f"User {userid} modified successfully.")
    return user_data

def modify_status(user_data, userid: str, session_active: bool):
    """Modify an existing user's session status in the user_data DataFrame and save to Excel."""
    #logger.debug(f"session_active= {session_active}")
    return modify_user(user_data, userid, session_active=session_active)

def delete_user(user_data, userid: str):
    """Delete a user from the user_data DataFrame and save to Excel."""
    if userid not in user_data['userid'].values:
        raise ValueError(f"User {userid} not found.")

    logger.info(f"Deleting user {userid} from DataFrame.")
    user_data = user_data[user_data['userid'] != userid]
    logger.info(f"User {userid} deleted. Saving changes to Excel.")
    save_user_data(user_data)
    logger.info(f"User {userid} deleted successfully.")
    return user_data

def get_user_info(user_data, userid: str):
    """Get user information from the user_data DataFrame."""
    userid = str(userid).strip()
    user_data['userid'] = user_data['userid'].astype(str).str.strip()
    user_info = user_data[user_data['userid'] == userid]
    if not user_info.empty and user_info['active'].iloc[0]:
        return user_info.iloc[0]
    return None

def get_user_info_1(user_data, userid: str):
    """Get user information from the user_data DataFrame (including inactive users)."""
    userid = str(userid).strip()
    user_data['userid'] = user_data['userid'].astype(str).str.strip()
    user_info = user_data[user_data['userid'] == userid]
    if not user_info.empty:
        logger.info(f"get_user_info_1()- Found user_info: {user_info.iloc[0]}")
    else:
        logger.info(f"get_user_info_1()- No matching user found for userid: '{userid}'")

    if not user_info.empty:
        return user_info.iloc[0]
    return None