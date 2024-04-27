from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Initialize an empty list to store the products
products = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded CSV file
        csv_file = request.files['csv_file']
        global products
        products = pd.read_csv(csv_file).to_dict('records')
        return render_template('product_list.html', products=products)
    return render_template('index.html')

@app.route('/product_list', methods=['GET', 'POST'])
def product_list():
    if request.method == 'POST':
        # Get the search query
        search_query = request.form['search_query']
        global products
        filtered_products = [product for product in products if search_query.lower() in product['name'].lower()]
        return render_template('product_list.html', products=filtered_products)
    return render_template('product_list.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    global products
    product = (product for product in products if product['id'] == product_id)
    if product:
        return render_template('product_detail.html', product=product)
    return 'Product not found', 404

if __name__ == '__main__':
    app.run()