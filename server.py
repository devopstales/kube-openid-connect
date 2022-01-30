from flask import Flask, session, redirect, session, request, render_template, g
import os
from requests_oauthlib import OAuth2Session
import yaml
import requests

oauth_server_uri = os.getenv("OAUTH_URI")
client_id = os.getenv("OAUTH_CLIENT_ID")
client_secret = os.getenv("OAUTH_CLIENT_SECRET")
redirect_uri = os.getenv("OAUTH_REDIRECT_URI", "http://localhost:5000/callback")
verify = os.getenv("OAUTH_CA_BUNDLE", False)
context = os.getenv("K8S_CONTEXT", False)

scope = [
    "openid",          # mandatory for OpenIDConnect auth
    "email",           # smallest and most consistent scope and claim
    "offline_access",  # needed to actually ask for refresh_token
    "good-service",
    "profile",
]

oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
auth_server_info = oauth.get(
    f"{oauth_server_uri}/.well-known/openid-configuration",
    withhold_token=True
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
    session['oauth_token'] = token

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
    config_snippet = {"users": [{"name": userinfo["preferred_username"], "user": kube_user}]}

    print("\nPaste/merge this user into your $KUBECONFIG\n")
    print(yaml.safe_dump(config_snippet))

    try:
      x = requests.post('http://%s:8080/' % request.remote_addr, json=config_snippet)
      print(x.text)
    except:
        print ("Print back error")

    return render_template(
        'index.html',
        user=userinfo["preferred_username"],
        context=context,
        user_snoppet=yaml.safe_dump(config_snippet)
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
  app.secret_key = os.urandom(24)
  app.run(host='localhost', port=5000,debug=True, use_reloader=False)
