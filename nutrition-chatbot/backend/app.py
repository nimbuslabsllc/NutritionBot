from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Load data from JSON
with open('menu_data.json', 'r') as file:
    menu_data = json.load(file)

@app.route('/get_product_info', methods=['GET'])
def get_product_info():
    product_name = request.args.get('name')
    product = next((p for p in menu_data if product_name.lower() in p['product_name'].lower()), None)
    return jsonify(product if product else {"error": "Product not found"})

@app.route('/filter_products', methods=['GET'])
def filter_products():
    exclude_allergens = request.args.getlist('allergens')
    filtered = [
        p for p in menu_data if not any(a in p['allergens'] for a in exclude_allergens)
    ]
    return jsonify(filtered)

@app.route('/list_categories', methods=['GET'])
def list_categories():
    categories = list(set(product['category'] for product in menu_data))
    return jsonify(categories)

if __name__ == '__main__':
    app.run(debug=True, port=5000)