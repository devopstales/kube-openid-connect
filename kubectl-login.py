#!/usr/bin/env python3
import webbrowser
import sys
import yaml
from flask import Flask, request
from waitress import serve
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/',methods = ['POST', 'GET'])
def hello_me():
    if request.method == 'POST':
        content = request['kube_user'].json
        print("\nPaste/merge this user into your $KUBECONFIG\n")
        print(yaml.safe_dump(content))
        print('(Press CTRL+C to quit)')
        return ''
    else:
      print ('else')
      return ''

if __name__ == '__main__':
    url=sys.argv[1]
    webbrowser.open(url)

    # debug mode
    # app.run(port=8080)

    # production mode
    serve(app, port=8080)