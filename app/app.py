from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config.from_pyfile('config/config.py')
cors = CORS(app)

db = SQLAlchemy(app)

@app.route('/')
@app.route('/home')
def index():
    return "Lazuli API V1"

from controllers.produtoController import *
from controllers.tipoProdutoController import *
from controllers.unidadeMedidaController import *
from controllers.compraController import *
from controllers.vendaController import *

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Erro interno do servidor'}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)