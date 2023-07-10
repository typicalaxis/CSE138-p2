from flask import Flask
import requests
from flask import request
import os

app = Flask(__name__)
PORT = 13800

FORWARDING_ADDRESS = ''
FORWARDING_ADDRESS = os.environ['FORWARDING_ADDRESS']
url = 'http://{}/kvs'.format(FORWARDING_ADDRESS)
testurl = 'http://{}/test'.format(FORWARDING_ADDRESS)
kvdict = {}

@app.route("/test")
def forward():
    return '{}'.format(FORWARDING_ADDRESS)

@app.route("/fortest")
def fortest():
    response = requests.get(testurl)
    return response.text

@app.route("/kvs", methods=['PUT'])
def kvs_put():
    data = request.get_json()
    if FORWARDING_ADDRESS != '':
        response = ''
        try:
            response = requests.put(url,json = data,verify=False, timeout=10)
        except:
            return {"error": "upstream down"}, 503
        else:
            return response.text, response.status_code
    else:
        if 'key' in data and 'val' in data:
            key = data['key']
            val = data['val']
            if key == None or val == None:
                return {"error": "bad PUT"}, 400
            elif len(key) > 200 or len(val) > 200:
                return {"error": "key or val too long"}, 400
            elif key in kvdict:
                oldval = kvdict[key]
                kvdict[key] = val
                return  {"replaced": True, "prev": oldval}, 200
            else:
                kvdict[key] = val
                return {"replaced": False}, 201
        else:
            return {"error": "bad PUT"}, 400

        


@app.route("/kvs", methods=['GET'])
def kvs_get():
    data = request.get_json()
    if FORWARDING_ADDRESS != '':
        response = ''
        try:
            response = requests.get(url,json = data,verify=False, timeout=10)
        except:
            return {"error": "upstream down"}, 503
        else:
            return response.text, response.status_code
    else:
        if 'key' in data:
            key = data['key']
            if key in kvdict:
                val = kvdict[key]
                return  {"val": val}, 200
            else:
                return {"error": "not found"}, 404
        else:
            return {"error": "bad GET"}, 400
    

@app.route("/kvs", methods=['DELETE'])
def kvs_delete():
    data = request.get_json()
    if FORWARDING_ADDRESS != '':
        response = ''
        try:
            response = requests.delete(url,json = data,verify=False, timeout=10)
        except:
            return {"error": "upstream down"}, 503
        else:
            return response.text, response.status_code
    else:
        if 'key' in data:
            key = data['key']
            if key in kvdict:
                val = kvdict[key]
                del kvdict[key]
                return  {"prev": val}, 200
            else:
                return {"error": "not found"}, 404
        else:
            return {"error": "bad DELETE"}, 400


if __name__ == "__main__":
    app.run(port = 13800, host = "0.0.0.0")