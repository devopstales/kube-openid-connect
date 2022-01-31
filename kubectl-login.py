#!/usr/bin/env python3
import webbrowser
import sys
import yaml
import platform
import os
from pathlib import Path
from flask import Flask, request
from waitress import serve
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/',methods = ['POST', 'GET'])
def hello_me():
    if request.method == 'POST':
        n = 0
        system = platform.system()
        if system == 'Darwin' or system == 'Linux':
            config_pah = os.path.expanduser('~/.kube/config')
            config_folder = os.path.expanduser('~/.kube')
        elif system == 'Windows':
            config_pah = os.path.expanduser('~\\.kube\\config')
            config_folder = os.path.expanduser('~\\.kube\\')
        
        if Path(config_pah).is_file():
            with open(config_pah) as fp:
                data = yaml.load(fp, Loader=yaml.FullLoader)
            
            content = request.json
            kube_user = content['kube_user']

            # merge users
            for i in data['users']:
                if i['name'] == kube_user['name']:
                    n += 1
            if n == 0:        
                print(n)
                data['users'].append(kube_user)
            # merge cluster
            # merge context
                
            # print to file

            #print("\nPaste/merge this user into your $KUBECONFIG\n")
            #print(yaml.safe_dump(data))
        elif Path(config_folder).is_dir():
            print()
            # create file from scratch
        else:
            print('Someting went wrong')
        
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