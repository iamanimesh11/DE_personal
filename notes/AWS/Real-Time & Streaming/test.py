import base64
import json

data = {"user_id": "user1", "event": "logout"}
json_data = json.dumps(data)
encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
print(encoded_data)
