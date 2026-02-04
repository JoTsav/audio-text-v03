import os
import requests
from cryptography.hazmat.primitives.serialization.ssh import load_application
from dotenv import load_dotenv
import json

load_dotenv()

PF_API_KEY = os.getenv("PURPLE_FABRIC_API_KEY")
USERNAME = os.getenv("PURPLE_FABRIC_USERNAME")
PASSWORD = os.getenv("PURPLE_FABRIC_PASSWORD")
BASE_URL = os.getenv("PURPLE_FABRIC_BASE_URL")

INVOKE_URL = os.getenv("INVOKE_URL")
GET_RESULT_URL = os.getenv("GET_RESULT_URL")

# TODO: Still not effectively retrieving bearer the token. MANUAL INSERTION WORKAROUND APPLIED
def get_bearer_token():
    """
    Fetches fresh token from Purple Fabric API
    :return:
    """
    token_url = f"{BASE_URL.rstrip('/')}/accesstoken"
    headers = {
        "apikey": PF_API_KEY,
        "username": USERNAME,
        "password": PASSWORD,
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(token_url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get("result") == "RESULT_SUCCESS":
                return data.get("access_token")
    except Exception as e:
        print(f"Error fetching bearer token: {e}")
    return os.getenv("PURPLE_FABRIC_BEARER_TOKEN") # fallback to env var



def send_to_purple_fabric(input_text):
    """Send transcribed text to Purple Fabric agent"""
    bearer_token = get_bearer_token()

    headers = {"apikey": PF_API_KEY, "Content-Type": "application/json",}
    if bearer_token:
        headers["Authorization"] =f"Bearer {bearer_token}"


    #Trying different paylod
    payload_options = [
        {"input": input_text},
        {"Input": input_text},
        {"text": input_text}, ]

    for payload in payload_options:
        try:
            response = requests.post(INVOKE_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            if response.status_code in (200, 201):
                return response.json()
        except Exception as e:
            print(f"Error sending to Purple Fabric: {e}")
    return None


def get_pf_result(trace_id):
    """Fetches the detailed result from the agent (beautified_output)"""
    if not trace_id or trace_id == os.getenv("PURPLE_FABRIC_TRACE_ID"):
        return None
    bearer_token = get_bearer_token()
    headers = {
        "apikey": PF_API_KEY,
        "Content-Type": "application/json",
    }
    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"

    url = f"{GET_RESULT_URL}{trace_id}"
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching result from Purple Fabric: {e}")
    return None

#### PyTest --------- FIX: Manual insertion of bearer
if __name__ == "__main__":
    sample_transcription = "Today I visited Ramesh Traders and discussed about gold loan renewal."
    result = send_to_purple_fabric(sample_transcription)
    print(result)
#####
