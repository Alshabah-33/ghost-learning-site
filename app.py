import os
import requests
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-before-deploying")

class QureoClient:
    BASE = "https://me-portal.qureo.education"
    def __init__(self):
        self.s = requests.Session()

    def login(self, username, password):
        # API endpoints can change; verify against the platform's current login flow.
        endpoints = [f"{self.BASE}/api/auth/login", f"{self.BASE}/api/login"]
        payload = {"username": username, "password": password}
        for url in endpoints:
            try:
                r = self.s.post(url, json=payload, timeout=20)
                if r.ok:
                    return True
            except requests.RequestException:
                pass
        return False

class SPXClient:
    BASE = "https://egy.app.spx-learning-square.com"
    def __init__(self):
        self.s = requests.Session()

    def login(self, username, password):
        # Placeholder integration: platform authentication details may change.
        endpoints = [f"{self.BASE}/api/auth/login", f"{self.BASE}/api/login"]
        payload = {"username": username, "password": password}
        for url in endpoints:
            try:
                r = self.s.post(url, json=payload, timeout=20)
                if r.ok:
                    return True
            except requests.RequestException:
                pass
        return False

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/login")
def qureo_login():
    data = request.get_json(silent=True) or {}
    username, password = data.get("username", ""), data.get("password", "")
    if not username or not password:
        return jsonify(ok=False, message="أدخل اسم المستخدم وكلمة المرور.")
    client = QureoClient()
    if not client.login(username, password):
        return jsonify(ok=False, message="تعذر تسجيل الدخول. قد تكون واجهة المنصة تغيّرت؛ تحقق من بياناتك وحاول لاحقًا."), 401
    session["qureo_logged_in"] = True
    return jsonify(ok=True, message="تم الاتصال بـ Qureo.")

@app.post("/api/spx-login")
def spx_login():
    data = request.get_json(silent=True) or {}
    username, password = data.get("username", ""), data.get("password", "")
    if not username or not password:
        return jsonify(ok=False, message="أدخل اسم المستخدم وكلمة المرور.")
    client = SPXClient()
    if not client.login(username, password):
        return jsonify(ok=False, message="تعذر الاتصال بـ SPX. قد تحتاج واجهة الدخول إلى تحديث."), 401
    session["spx_logged_in"] = True
    return jsonify(ok=True, message="تم الاتصال بـ SPX.")

@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify(ok=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
