from flask import Flask, request, jsonify
from xmlrpc import client as xmlrpclib
from datetime import datetime

app = Flask(__name__)

# Connection data for Odoo
data_url = 'enter Odoo URL here'
database = 'enter Odoo database name here'
user = 'enter Odoo username here'
password = 'enter Odoo API key here'

# Connection to Odoo using XML-RPC
common = xmlrpclib.ServerProxy(f'{data_url}xmlrpc/2/common')
uid = common.authenticate(database, user, password, {})
models = xmlrpclib.ServerProxy(f'{data_url}xmlrpc/2/object')

# Counter for the incremental ID of the lot
current_year = datetime.now().year
lote_counter = 1  # Initialize the counter

def create_lot(lot_name, product_id):
    lot_vals = {
        'name': lot_name,
        'product_id': product_id,
    }
    lot_id = models.execute_kw(database, uid, password, 'stock.lot', 'create', [lot_vals])
    return lot_id

# Route to receive REST data
@app.route('/inventoryAdjustments', methods=['POST'])
def receive_data():
    try:
        global lote_counter  # Reference the global variable
        data_json = request.json  # Define data_json here

        article = data_json['article']

        # Get the product ID based on the 'article' variable
        product_ids = models.execute_kw(database, uid, password, 'product.product', 'search', [[['default_code', '=', article]]], {'limit': 1})

        if not product_ids:
            raise Exception(f'Product not found with name: {article}')

        # Create a lot with the same value as lote_counter
        global lote_counter  # Reference the global variable
        lote_counter_str = str(lote_counter).zfill(4)  # Fill with zeros
        lot = f'{current_year}{lote_counter_str}'
        lote_counter += 1  # Increment the counter

        linear_meters = data_json['linear_meters']
        cant_float = float(linear_meters)

        # Create a new record in mrp.production
        production_order_vals = {
            'product_id': product_ids[0],  # Take the first product ID
            'lot_producing_id': 1,
            'product_qty': cant_float
        }
        stock_quant_id = models.execute_kw(database, uid, password, 'mrp.production', 'create', [production_order_vals])

        # Create a new lot
        lot_id = create_lot(lot, product_ids[0])

        print({'Status': 'Uploaded Successfully', 'Product': article, 'Lot': lot})
        return jsonify({'Status': 'Uploaded Successfully', 'Product': article, 'Lot': lot})

    except Exception as e:
        print("NOT OK: ", e)
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="192.168.1.24", port=5003, threads=80)
