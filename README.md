### Kube OpenID Connect

Kube OpenID Connect is an application that can be used to easily enable authentication flows via OIDC for a kubernetes cluster. Kubernetes supports [OpenID Connect Tokens](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#openid-connect-tokens) as a way to identify users who access the cluster. Kube OpenID Connect helps users with it's plugin to authenticate an get `kubectl` config.

![Kube OpenID Connect screenshot](docs/images/screenshot.png)

### Deployment

### How It Works

### Build executable

```
pip3 install -r requirements.txt
pyinstaller --onefile --noconfirm --noconsole --clean --log-level=WARN --key=MySuperSecretPassword --strip kubectl-login.py
```
