from flask import Flask, jsonify
import requests

API_IBGE = "https://servicodados.ibge.gov.br/api/v2/cnae/subclasses/{}"

app = Flask(__name__)

def consulta_cnae(codigo: str):
    """Consulta CNAE na API do IBGE e devolve dict ou None."""
    codigo = codigo.replace(".", "").replace("-", "")
    url = API_IBGE.format(codigo)
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException:
        return None

    data = resp.json()
    if isinstance(data, list) and data:
        item = data[0]
        return {
            "codigo": item["id"],
            "descricao": item["descricao"],
            "secao": item["classe"]["grupo"]["divisao"]["secao"]["descricao"],
            "divisao": item["classe"]["grupo"]["divisao"]["descricao"],
            "grupo": item["classe"]["grupo"]["descricao"],
            "classe": item["classe"]["descricao"]
        }
    return None

@app.route("/cnae/<codigo>")
def get_cnae(codigo):
    resultado = consulta_cnae(codigo)
    if resultado:
        return jsonify(resultado)
    return jsonify({"erro": "CNAE não encontrado"}), 404

@app.route("/")
def index():
    return jsonify({"message": "API CNAE - use /cnae/<codigo>"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
