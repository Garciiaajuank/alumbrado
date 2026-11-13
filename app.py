import os
from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)