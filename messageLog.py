import requests
from dotenv import load_dotenv
import os

load_dotenv()
messageLogUrl = os.getenv("MESSAGE_LOG_URL") or "https://simp-admin.herokuapp.com/api/logs"

def MessageLog(name, section, log_message='', log_json=''):
    msg = { 
        'data' :
           {
                'name': name,
                'section': section,
                'log_message': log_message,
                'log_json': log_json
            }
    }
    result = requests.post(messageLogUrl, json=msg)
    return result
