from flask import Flask, render_template
from flask_socketio import SocketIO
from kafka import KafkaConsumer
import json
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Kafka consumer
def consume_kafka():
    consumer = KafkaConsumer(
        'location_updates',
        bootstrap_servers=['172.19.165.234:9092'],  # Replace with your Kafka broker address
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    for message in consumer:
        # Broadcast the location update to connected clients
        socketio.emit('location_update', message.value)
        print(f"Broadcasted: {message.value}")

# Start Kafka consumer in a separate thread
thread = threading.Thread(target=consume_kafka)
thread.daemon = True
thread.start()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
