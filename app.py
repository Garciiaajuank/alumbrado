import os, time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

ESTADO = {"postes": [], "actualizado": 0}
API_KEY = os.environ.get("API_KEY", "alumbrado2026")


@app.route("/")
def inicio():
    return render_template("inicio.html", active="inicio")


@app.route("/proyecto")
def proyecto():
    return render_template("proyecto.html", active="proyecto")


@app.route("/maqueta")
def maqueta():
    return render_template("maqueta.html", active="maqueta")


@app.route("/envivo")
def envivo():
    return render_template("envivo.html", active="envivo")


@app.route("/bases-de-datos")
def bases_datos():
    return render_template("bases_datos.html", active="bases_datos")


@app.route("/dw-y-etl")
def dw_etl():
    return render_template("dw_etl.html", active="dw_etl")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", active="dashboard")


@app.route("/conocimientos")
def conocimientos():
    return render_template("conocimientos.html", active="conocimientos")


@app.route("/resultados")
def resultados():
    return render_template("resultados.html", active="resultados")


@app.route("/api/estado", methods=["POST"])
def recibir_estado():
    if request.headers.get("X-API-Key") != API_KEY:
        return jsonify(error="no autorizado"), 401
    datos = request.get_json(force=True, silent=True) or {}
    ESTADO["postes"] = datos.get("postes", [])
    ESTADO["actualizado"] = time.time()
    return jsonify(ok=True)


@app.route("/api/estado", methods=["GET"])
def leer_estado():
    respuesta = jsonify({**ESTADO, "ahora": time.time()})
    respuesta.headers["Cache-Control"] = "no-store"
    return respuesta


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)