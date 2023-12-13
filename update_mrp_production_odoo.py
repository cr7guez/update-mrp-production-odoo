from flask import Flask, request, jsonify
from xmlrpc import client as xmlrpclib
from datetime import datetime

app = Flask(__name__)

# Datos de conexión a Odoo
data_url = 'http://95.62.94.92:8069/'
database = 'Tubau_V16'
user = 'lluis.gomez@lancer-digital.com'
password = '906d47c104a5e9b6eced41388b7094ae10dc3d26'

# Conexión a Odoo mediante XML-RPC
common = xmlrpclib.ServerProxy(f'{data_url}xmlrpc/2/common')
uid = common.authenticate(database, user, password, {})

models = xmlrpclib.ServerProxy(f'{data_url}xmlrpc/2/object')

# Contador para el ID incremental del lote
current_year = datetime.now().year
lote_counter = 1  # Inicializar el contador

def crear_lote(nombre_lote, producto_id):
    data_json = request.json  # Definir data_json aquí
    lote = data_json['lote']
    lote_vals = {
        'name': lote,
        'product_id': producto_id,
    }
    lote_id = models.execute_kw(database, uid, password, 'stock.lot', 'create', [lote_vals])
    return lote_id

# Ruta para recibir datos REST
@app.route('/ajustesInventario', methods=['POST'])
def recepcion_datos():
    try:
        global lote_counter  # Hacer referencia a la variable global
        data_json = request.json  # Definir data_json aquí

        articulo = data_json['articulo']

        # Obtener el ID del producto a partir de la variable 'articulo'
        producto_ids = models.execute_kw(database, uid, password, 'product.product', 'search', [[['default_code', '=', articulo]]], {'limit': 1})

        if not producto_ids:
            raise Exception(f'No se encontró el producto con nombre: {articulo}')

        # Crear un lote con el mismo valor que lote_counter
        # global lote_counter  # Hacer referencia a la variable global
        # lote_counter_str = str(lote_counter).zfill(4)  # Rellenar con ceros
        # lote = f'{current_year}{lote_counter_str}'
        # lote_counter += 1  # Incrementar el contador

        metros_lineales = data_json['metros_lineales']
        cant_float = float(metros_lineales)

        # Crear un nuevo registro en mrp.production
        production_order_vals = {
            'product_id': producto_ids[0],  # Tomar el primer identificador de producto
            'lot_producing_id': 1,
            'product_qty': cant_float
        }
        stock_quant_id = models.execute_kw(database, uid, password, 'mrp.production', 'create', [production_order_vals])

        lote = data_json['lote']
        cantidad = data_json['cantidad']
        bobina = data_json['bobina']
        
        # Crear un nuevo lote
        lote_id = crear_lote(lote, producto_ids[0])

        print({'Estado': 'Súbido Correctamente', 'Producto': articulo, 'Lote': lote})
        return jsonify({'Estado': 'Súbido Correctamente', 'Producto': articulo, 'Lote': lote})

    except Exception as e:
        print("NO OK: ", e)
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="192.168.1.24", port=5003, threads=80)
