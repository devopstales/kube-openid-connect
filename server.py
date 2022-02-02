from flask import Flask, session, redirect, session, request, render_template, Response
import os

from itsdangerous import base64_decode
from requests_oauthlib import OAuth2Session
import yaml
import requests

oauth_server_uri = os.getenv("OAUTH_URI")
client_id = os.getenv("OAUTH_CLIENT_ID")
client_secret = os.getenv("OAUTH_CLIENT_SECRET")
redirect_uri = os.getenv("OAUTH_REDIRECT_URI", "http://localhost:5000/callback")
verify = os.getenv("OAUTH_CA_BUNDLE", False)
context = os.getenv("K8S_CONTEXT")
base64_k8s_server_ca = os.getenv("K8S_SERVER_CA")
k8s_server_url = os.getenv("K8S_SERVER_URL")

scope = [
    "openid",          # mandatory for OpenIDConnect auth
    "email",           # smallest and most consistent scope and claim
    "offline_access",  # needed to actually ask for refresh_token
    "good-service",
    "profile",
]
k8s_server_ca=str(base64_decode(base64_k8s_server_ca), 'UTF-8')

oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
auth_server_info = oauth.get(
    f"{oauth_server_uri}/.well-known/openid-configuration",
    withhold_token=True,
    verify=verify
).json()
# print ('%s' % auth_server_info) # deebug

app = Flask(__name__)

@app.route('/')
def index():
    auth_url = auth_server_info["authorization_endpoint"]

    authorization_url, state = oauth.authorization_url(
        auth_url,
        access_type="offline",  # not sure if it is actually always needed,
                                # may be a cargo-cult from Google-based example
    )
    session['oauth_state'] = state
    return redirect(authorization_url)


@app.route("/callback", methods=["GET"])
def callback():
    token_url = auth_server_info["token_endpoint"]
    userinfo_url = auth_server_info["userinfo_endpoint"]

    token = oauth.fetch_token(
        token_url,
        authorization_response=request.url,
        client_secret=client_secret,
        timeout=60,
        verify=verify,
    )

    # discover user info
    userinfo = oauth.get(
        userinfo_url,
        timeout=60,
        verify=verify,
    ).json()

    # print ('%s' % userinfo) # debug

    kube_user = {
        "auth-provider": {
            "name": "oidc",
            "config": {
                "client-id": client_id,
                "idp-issuer-url": oauth_server_uri,
                "id-token": token["id_token"],
                "refresh-token": token.get("refresh_token"),
            }
        }
    }
    if client_secret:
        kube_user["auth-provider"]["config"]["client-secret"] = client_secret
    if verify:
        kube_user["auth-provider"]["config"]["idp-certificate-authority"] = verify

    kube_cluster = {
        "certificate-authority-data": base64_k8s_server_ca,
        "server": k8s_server_url
    }

    kube_context = {
        "cluster": context,
        "user": context,
    }

    user_config_snippet = {"name": context, "user": kube_user}
    cluster_config_snippet = {"name": context, "cluster": kube_cluster}
    context_config_snippet = {"name": context, "context": kube_context}

    #print(yaml.safe_dump(user_config_snippet)) # debug

    try:
      x = requests.post('http://%s:8080/' % request.remote_addr, json={
            "kube_user": user_config_snippet,
            "kube_cluster": cluster_config_snippet,
            "kube_context": context_config_snippet,
            "context": context
          }
        )
      print(x.text)
    except:
        print ("Kubectl print back error")

    session['oauth_token'] = token
    session['refresh_token'] = token.get("refresh_token")
    return render_template(
        'index.html',
        preferred_username=userinfo["preferred_username"],
        redirect_uri=redirect_uri,
        client_id=client_id,
        client_secret=client_secret,
        id_token=token["id_token"],
        refresh_token=token.get("refresh_token"),
        oauth_server_uri=oauth_server_uri,
        context=context,
        k8s_server_url=k8s_server_url,
        k8s_server_ca=k8s_server_ca
    )

@app.route("/get-file")
def get_file():
    oauth = OAuth2Session()
    auth_server_info = oauth.get(
        f"{oauth_server_uri}/.well-known/openid-configuration",
        withhold_token=True,
        verify=verify,
        timeout=60,
    ).json()

    token_url = auth_server_info["token_endpoint"]

    token = oauth.refresh_token(
        token_url=token_url,
        refresh_token=session['refresh_token'],
        client_id=client_id,
        client_secret=client_secret,
        verify=verify,
        timeout=60,
    )

    kube_user = {
            "auth-provider": {
                "name": "oidc",
                "config": {
                    "client-id": client_id,
                    "idp-issuer-url": oauth_server_uri,
                    "id-token": token["id_token"],
                    "refresh-token": token.get("refresh_token"),
                }
            }
        }
    if client_secret:
        kube_user["auth-provider"]["config"]["client-secret"] = client_secret
    if verify:
        kube_user["auth-provider"]["config"]["idp-certificate-authority"] = verify
    
    kube_cluster = {
        "certificate-authority-data": base64_k8s_server_ca,
        "server": k8s_server_url
    }

    kube_context = {
        "cluster": context,
        "user": context,
    }

    config_snippet = {
        "apiVersion": "v1",
        "kind": "Config",
        "clusters": [{
            "name": context,
            "cluster": kube_cluster
        }],
        "contexts": [{
            "name": context,
            "context": kube_context
        }],
        "current-context": context,
        "preferences": {},
        "users": [{
            "name": context,
            "user": kube_user
        }]
    }

    #session['oauth_token'] = token
    return Response(
            yaml.safe_dump(config_snippet),
            mimetype="text/yaml",
            headers={
                "Content-Disposition":
                "attachment;filename=kubecfg.yaml"
            }
    )

@app.route('/logout')
def logout():
    logout_url = auth_server_info["end_session_endpoint"]
    hosturl = 'http%3A%2F%2Flocalhost%3A5000%2F'
    session.pop('oauth_token')

    return redirect(
        logout_url + '?redirect_uri=' + hosturl)

if __name__ == '__main__':
    os.environ['DEBUG'] = '1'
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    # app.secret_key = os.urandom(24)
    app.secret_key = 'development'
    app.run(host='localhost', port=5000,debug=True, use_reloader=False)
