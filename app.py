import os
import time
from threading import Lock
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY", "alumbrado2026")

# Estado compartido entre el POST del ESP32 y el GET de la página
ESTADO = {
    "postes": [],
    "fase_actual": None,
    "postes_activos": 0,
    "consumo_total_kw": 0.0,
    "uptime_ms": 0,
    "dispositivo": "",
    "actualizado": 0,
}
ESTADO_LOCK = Lock()


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
    # Validación segura de la API Key
    if request.headers.get("X-API-Key") != API_KEY:
        return jsonify(error="no autorizado"), 401

    datos = request.get_json(force=True, silent=True)
    
    # Si el ESP32 no envió un JSON válido, evitamos romper el estado actual
    if not isinstance(datos, dict):
        return jsonify(error="payload invalido"), 400

    with ESTADO_LOCK:
        # Actualizamos solo si vienen los datos de postes para evitar sobreescrituras vacías
        if "postes" in datos:
            ESTADO["postes"] = datos.get("postes", [])
            
        ESTADO["fase_actual"] = datos.get("fase_actual", ESTADO["fase_actual"])
        ESTADO["postes_activos"] = datos.get("postes_activos", ESTADO["postes_activos"])
        ESTADO["consumo_total_kw"] = datos.get("consumo_total_kw", ESTADO["consumo_total_kw"])
        ESTADO["uptime_ms"] = datos.get("uptime_ms", ESTADO["uptime_ms"])
        ESTADO["dispositivo"] = datos.get("dispositivo", ESTADO["dispositivo"])
        ESTADO["actualizado"] = time.time()

    return jsonify(ok=True)


@app.route("/api/estado", methods=["GET"])
def leer_estado():
    with ESTADO_LOCK:
        copia = dict(ESTADO)
    respuesta = jsonify({**copia, "ahora": time.time()})
    respuesta.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    respuesta.headers["Pragma"] = "no-cache"
    return respuesta


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # threaded=True permite atender simultáneamente al navegador y al ESP32 sin bloqueos
    app.run(host="0.0.0.0", port=port, threaded=True, debug=True)