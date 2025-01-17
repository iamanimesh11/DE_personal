from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

@app.route('/send_location', methods=['POST'])
def receive_location():
    data = request.get_json()
    print(f"Received data: {data}")
    return jsonify({"status": "success", "received": data}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
