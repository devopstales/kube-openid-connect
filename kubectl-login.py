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
def index():
    if request.method == 'POST':
        system = platform.system()
        if system == 'Darwin' or system == 'Linux':
            config_pah = os.path.expanduser('~/.kube/config')
            config_folder = os.path.expanduser('~/.kube')
        elif system == 'Windows':
            config_pah = os.path.expanduser('~\\.kube\\config')
            config_folder = os.path.expanduser('~\\.kube\\')

        content = request.json
        kube_user = content['kube_user']
        kube_cluster = content['kube_cluster']
        kube_context = content['kube_context']
        context = content['context']

        if Path(config_pah).is_file():
            with open(config_pah) as fp:
                data = yaml.load(fp, Loader=yaml.FullLoader)
            # merge users
            n = 0
            for i in data['users']:
                if i['name'] == kube_user['name']:
                    n += 1
            if n == 0:        
                data['users'].append(kube_user)
                data['clusters'].append(kube_cluster)
                data['contexts'].append(kube_context)
                #print(yaml.safe_dump(data)) # debug
                print("Write config for %s to %s" % (kube_user['name'], config_pah))
                file = open(config_pah, "w")
                yaml.dump(data, file)
            else:
                print("Config for %s already exists" % kube_user['name'])
        elif Path(config_folder).is_dir():
            config_snippet = {
                "apiVersion": "v1",
                "kind": "Config",
                "clusters": [],
                "contexts": [],
                "current-context": context,
                "preferences": {},
                "users": []
            }
            config_snippet['users'].append(kube_user)
            config_snippet['clusters'].append(kube_cluster)
            config_snippet['contexts'].append(kube_context)
            print("Create config file with config for %s to %s" % (kube_user['name'], config_pah))
            file = open(config_pah, "w+")
            yaml.dump(config_snippet, file)
        else:
            os.makedirs(config_folder)
            config_snippet = {
                "apiVersion": "v1",
                "kind": "Config",
                "clusters": [],
                "contexts": [],
                "current-context": context,
                "preferences": {},
                "users": []
            }
            config_snippet['users'].append(kube_user)
            config_snippet['clusters'].append(kube_cluster)
            config_snippet['contexts'].append(kube_context)
            print("Create folder and config file with config for %s to %s" % (kube_user['name'], config_pah))
            file = open(config_pah, "w+")
            yaml.dump(config_snippet, file)
        
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