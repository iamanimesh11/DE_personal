# # import string
# # import random
# #
# # # using random.choices() generating random strings
# # res = ''.join(random.choices(string.ascii_letters,
# #                              k=7)) # initializing size of string
# #
# # print(str(res))
# import requests
# import json
# import time
#
# # Your Discord Webhook URL (replace with your own URL)
# WEBHOOK_URL = "https://discord.com/api/webhooks/1324620959298355320/F2jHs-D-EPSf0MPlNaOWUuyf4FYWI-7vOCrmQbfTK12QggTIAabhUjI61nQtCPE_6CY8"
#
# # The message you want to send
#
#
# # Loop to send the message 50 times
# for i in range(50):
#     message = "Hello,  message "+str(i)+" from my Python script!"
#
#     # Create the payload (content of the message)
#     payload = {
#         "content": message
#     }
#     # Send the POST request to Discord Webhook URL
#     response = requests.get(WEBHOOK_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"},verify=False)
#
#     # Check if the request was successful
#     if response.status_code == 204:
#         print(f"Message {i + 1} successfully sent!")
#     else:
#         print(f"Failed to send message {i + 1}. Status code: {response.status_code}")
#
#     # Optional: Adding a delay of 1 second to avoid flooding the server too quickly
#     time.sleep(1)



import discord

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

client.run('MTMyNTY5NDQ2ODcwMzEyOTcwNA.GOpfzN.UmkYZZTBnhMc9rDkzc7DQ2odiWVeLX9m7dIKAk')