import sys
import json
import logging
from bottle import Bottle, request, HTTPResponse, HTTPError

args = sys.argv
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
    version = "v" + args[1]
    logging.info("### Response: method=[get_version], version=[{0}]".format(version))
    return makeResponse(200, version, "plain")

@app.get('/info')
@app.get('/info/')
def get_info():
    name = "Study-of-GitOps"
    version = "v" + args[1]
    date = "2023/4/15"
    info_dict = {"name": name, "version": version, "date": date}
    
    return makeResponse(200, info_dict, "json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
