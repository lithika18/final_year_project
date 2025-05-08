from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load data once when server starts
df = pd.read_csv("lithika.csv")
df['price'] = pd.to_numeric(df['price'], errors='coerce')

@app.route('/recommend', methods=['GET'])
def recommend_cheaper():
    product_name = request.args.get('product')
    product = df[df['name'].str.lower() == product_name.lower()]

    if product.empty:
        return jsonify({"error": "Product not found."}), 404

    category = product['collection'].values[0]
    price = product['price'].values[0]

    cheaper_alts = df[
        (df['collection'] == category) &
        (df['name'].str.lower() != product_name.lower()) &
        (df['price'] < price)
    ].sort_values(by='price')

    results = cheaper_alts[['name', 'price']].head(3).to_dict(orient='records')
    return jsonify(results)