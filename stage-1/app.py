from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/api/hello', strict_slashes=False)
def index():
    """
    Greet user from the query string and provide weather information based on IP address
    """

    name = request.args.get('visitor_name')
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

    api_key = os.getenv('KEY')
    url = f'http://api.weatherapi.com/v1/current.json?key={api-key}&q={ip}'
    data = requests.get(url).json()
    location = data.get('location', {})
    current = data.get('current', {})
    temp = current.get('temp_c')
    state = location.get('name')

    obj = {
         "client_ip": ip,
        "location": location.get('name'),
        "greeting": f"Hello, {name}!, the temperature is {temp} degrees Celsius in {state}."
            }

    return jsonify(obj), 200

if __name__ == '__main__':
    app.run(debug=True)

