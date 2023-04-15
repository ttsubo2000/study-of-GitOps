import json
import logging
from bottle import Bottle, request, HTTPResponse, HTTPError

app = Bottle()

def makeResponse(code, data, type):
    if type == "plain":
        r = HTTPResponse(status=code, body="{0}\n".format(data))
        r.set_header('Content-Type', 'text/plain')
    elif type == "json":
        body = json.dumps(data) + "\n"
        r = HTTPResponse(status=code, body=body)
        r.set_header('Content-Type', 'application/json')
    return r

@app.get('/')
def get_version():
    version = "v1.0.1"
    logging.info("### Response: method=[get_version], version=[{0}]".format(version))
    return makeResponse(200, version, "plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
