import os
import sys

from flask import Flask, request, jsonify

from utils.conversions import c2f
from utils.conversions import f2c
from utils.msteams_verify import verify_hmac

app = Flask(__name__)

try:
    MSTEAMS_TOKEN = os.environ['MSTEAMS_TOKEN']
except KeyError:
    print('Please define the environment variable MSTEAMS_TOKEN')
    sys.exit(1)


@app.route('/')
def hello_world():
    return 'Hello from Flask!'


@app.route('/webhook', methods=['POST'])
@verify_hmac(MSTEAMS_TOKEN)
def webhook():
    req = request.json.get('text').split('tc')[1].strip()
    temperature, temperature_scale = req[:-1], req[-1]
    temperature = float(''.join(ele for ele in temperature if ele.isdigit() or ele == '.' or ele == '-'))
    if temperature_scale == 'c':
        if temperature >= -273.15:
            return jsonify({"type": "message", "text": f"{c2f(temperature):.1f}f"})
        else:
            return jsonify({"type": "message", "text": "Trying to subvert absolute zero? Well try again, pal."})
    elif temperature_scale == 'f':
        if temperature >= -459.67:
            return jsonify({"type": "message", "text": f"{f2c(temperature):.1f}c"})
        else:
            return jsonify({"type": "message", "text": "Trying to subvert absolute zero? Well try again, pal."})
    else:
        return jsonify({"type": "message", "text": f"Please format like -40c or 98.6f"})
