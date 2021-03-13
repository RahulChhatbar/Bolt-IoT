import requests
import json
import time
from boltiot import Bolt
import alert

mybolt = Bolt(alert.bolt_api_key, alert.device_id)

def get_value_from_ldr(pin):
    try:
        response = mybolt.analogRead(pin)
        data = json.loads(response)
        if data["success"] != 1:
            print("Request not successfull")
            print("This is the response->", data)
            return -999
        ldr_reading = int(data["value"])
        return ldr_reading
    except Exception as e:
        print("Something Went Wrong.")
        print(e)
        return -999


def sms_alert(message):
    url = "https://api.telegram.org/" + alert.telegram_bot_id + "/sendMessage"
    data = {
        "chat_id": alert.telegram_chat_id,
        "text": message
    }
    try:
        response = requests.request(
            "POST",
            url,
            params=data
        )
        print("This is the Telegram URL")
        print(url)
        print("This is the Telegram response")
        print(response.text)
        telegram_data = json.loads(response.text)
        return telegram_data["ok"]
    except Exception as e:
        print("An error occurred in sending the alert message via Telegram")
        print(e)
        return False


while True:
    
    ldr_reading = get_value_from_ldr("A0")    
    
    if ldr_reading == -999:
        print("Please check your bolt module. Skipping.")
        time.sleep(5)
        continue
    
    if ldr_reading >= alert.threshold:
        print("Sensor value has exceeded threshold")
        message = "Alert! Your locker/vault has been breached."
        telegram_status = sms_alert(message)
        print("This is the Telegram status:", telegram_status)

    time.sleep(5)