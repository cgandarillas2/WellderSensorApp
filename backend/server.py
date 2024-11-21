from flask import Flask, jsonify
from flask_cors import CORS  # Importa flask-cors
import serial

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

arduino_port = "/dev/cu.usbserial-1410"  # Cambia según el puerto detectado
baud_rate = 57600
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

@app.route('/status', methods=['GET'])
def get_room_status():
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()
        try:
            # Evalúa los datos como JSON
            room_data = eval(data)  # Si prefieres seguridad, usa json.loads
            return jsonify(room_data)
        except Exception as e:
            return jsonify({"error": "Invalid data format", "raw_data": data})
    return jsonify({"Room1": "Unknown"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

