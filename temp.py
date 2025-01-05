# import string
# import random
#
# # using random.choices() generating random strings
# res = ''.join(random.choices(string.ascii_letters,
#                              k=7)) # initializing size of string
#
# print(str(res))
import requests
import json
import time

# Your Discord Webhook URL (replace with your own URL)
WEBHOOK_URL = "https://discord.com/api/webhooks/1324620959298355320/F2jHs-D-EPSf0MPlNaOWUuyf4FYWI-7vOCrmQbfTK12QggTIAabhUjI61nQtCPE_6CY8"

# The message you want to send


# Loop to send the message 50 times
for i in range(50):
    message = "Hello,  message "+str(i)+" from my Python script!"

    # Create the payload (content of the message)
    payload = {
        "content": message
    }
    # Send the POST request to Discord Webhook URL
    response = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"})

    # Check if the request was successful
    if response.status_code == 204:
        print(f"Message {i + 1} successfully sent!")
    else:
        print(f"Failed to send message {i + 1}. Status code: {response.status_code}")

    # Optional: Adding a delay of 1 second to avoid flooding the server too quickly
    time.sleep(1)
