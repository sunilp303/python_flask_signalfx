#coding: utf-8
from flask import Flask, jsonify
from flask_restplus import reqparse
import requests


app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True


def validate(id):
    idr = str(id)
    if idr.startswith( 'i-' ):
        return id
    else:
        raise ValueError('Should be not empty and start with "i-"')

@app.route("/", methods=['POST'])
def parseAwsHealthCheck():
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('id', required=True, type=validate,  help="ID cannot be blank! {error_msg}")
    parser.add_argument('description', required=True, help='Description cannot be blank!')
    args = parser.parse_args(strict=True)
    datai = [{
        "category": "ALERT",
        "eventType": "AWS",
        "properties": {
            "id": args.id, "description": args.description
        }
    }]
    headers = { "Content-Type": "application/json", "X-SF-Token": "XXXXXXXXXXXXX"}
    r = requests.post('https://ingest.us1.signalfx.com/v2/event', json=datai, headers=headers)
    return jsonify({"status": "success"})