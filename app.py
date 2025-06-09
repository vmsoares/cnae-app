from flask import Flask, jsonify
import requests

API_IBGE = "https://servicodados.ibge.gov.br/api/v2/cnae/subclasses/{}"

app = Flask(__name__)

def consulta_cnae(codigo: str):
    """Consulta CNAE na API do IBGE e devolve dict ou None."""
    codigo = codigo.replace(".", "").replace("-", "")
    url = API_IBGE.format(codigo)
    resp = requests.get(url, timeout=10)
    if resp.status_code == 200:
        data = resp.json()
        if data:                       # lista com um item
            return {
                "codigo": data[0]["id"],
                "descricao": data[0]["descricao"],
                "secao": data[0]["classe"]["grupo"]["divisao"]["secao"]["descricao"],
                "divisao": data[0]["classe"]["grupo"]["divisao"]["descricao"],
                "grupo": data[0]["classe"]["grupo"]["descricao"],
                "classe": data[0]["classe"]["descricao"]
            }
    return None

@app.route("/cnae/<codigo>")
def get_cnae(codigo):
    resultado = consulta_cnae(codigo)
    if resultado:
        return jsonify(resultado)
    return jsonify({"erro": "CNAE não encontrado"}), 404
@app.route("/")
def i.ndex():
    return jsonify({"message": "API CNAE - use /cnae/<codigo>"})
    if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

__name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
