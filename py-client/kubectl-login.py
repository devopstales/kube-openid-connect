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
from itsdangerous import base64_encode
import validators

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
        context = content['context']
        k8s_server_url = content['server']
        k8s_server_ca = content['certificate-authority-data']
        client_id = content['client-id']
        id_token =  content['id-token']
        refresh_token =  content['refresh-token']
        oauth_server_uri =  content['idp-issuer-url']
        client_secret =   content['client_secret']

        if Path(config_pah).is_file():
            with open(config_pah) as fp:
                data = yaml.load(fp, Loader=yaml.FullLoader)
                kube_user = {
                        "auth-provider": {
                            "name": "oidc",
                            "config": {
                                "client-id": client_id,
                                "idp-issuer-url": oauth_server_uri,
                                "id-token": id_token,
                                "refresh-token": refresh_token,
                            }
                        }
                    }
                kube_user["auth-provider"]["config"]["client-secret"] = client_secret
                base64_k8s_server_ca=str(base64_encode(k8s_server_ca), 'UTF-8')
                kube_cluster = {
                    "certificate-authority-data": base64_k8s_server_ca,
                    "server": k8s_server_url
                }
                kube_context = {
                    "cluster": context,
                    "user": context,
                }
            # merge users
            n = 0
            for i in data['contexts']:
                if i['name'] == context:
                    n += 1

            if n == 0:        
                data['users'].append(kube_user)
                data['clusters'].append(kube_cluster)
                data['contexts'].append(kube_context)
                #print(yaml.safe_dump(data)) # debug
                print("Write config for %s to %s" % (context, config_pah))
                file = open(config_pah, "w")
                yaml.dump(data, file)
            else:
                print("Config for %s already exists" % context)
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
            print("Create config file with config for %s to %s" % (context, config_pah))
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
            print("Create folder and config file with config for %s to %s" % (context, config_pah))
            file = open(config_pah, "w+")
            yaml.dump(config_snippet, file)
        
        print('Happy Kubernetes interaction!')
        print('(Press CTRL+C to quit)')
        #exit()
        return ''
    else:
      print ('else')
      return ''

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if validators.url(sys.argv[1]):
            url=sys.argv[1]
        else:
            print("Argument is not a valid url")
            exit(2)
    else:
       print("Incorrect Number of Arguments Provided")
       exit(2)


    
    webbrowser.open(url)

    # debug mode
    # app.run(port=8080)

    # production mode
    serve(app, port=8080)