```bash
pip3 install -r requirements.txt
```

### Build executable

```
pyinstaller --onefile --noconfirm --noconsole --clean --log-level=WARN --key=MySuperSecretPassword --strip kubectl-login.py
```

---
* https://pshchelo.github.io/pykube-oidc-refresh.html
* kubernetes oidc python
