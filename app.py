from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Product, Supplier, Transaction, init_db
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mini_erp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-key'
db.init_app(app)

# Initialize database when the app starts (Flask 3.x compatible)
with app.app_context():
    init_db(app)

@app.route('/')
def dashboard():
    total_products = Product.query.count()
    low_stock = Product.query.filter(Product.quantity <= Product.reorder_level).all()
    total_value = db.session.query(func.sum(Product.quantity * Product.price)).scalar() or 0
    return render_template('dashboard.html', total_products=total_products, low_stock=low_stock, total_value=total_value)

# Products CRUD
@app.route('/products')
def products():
    products = Product.query.all()
    suppliers = Supplier.query.all()
    return render_template('products.html', products=products, suppliers=suppliers)

@app.route('/products/add', methods=['POST'])
def add_product():
    name = request.form.get('name')
    sku = request.form.get('sku')
    price = float(request.form.get('price') or 0)
    quantity = int(request.form.get('quantity') or 0)
    reorder_level = int(request.form.get('reorder_level') or 0)
    supplier_id = request.form.get('supplier_id') or None
    if not name or not sku:
        flash('Name and SKU are required', 'danger')
        return redirect(url_for('products'))
    p = Product(name=name, sku=sku, price=price, quantity=quantity, reorder_level=reorder_level)
    if supplier_id:
        s = Supplier.query.get(int(supplier_id))
        if s:
            p.supplier = s
    db.session.add(p)
    db.session.commit()
    flash('Product added', 'success')
    return redirect(url_for('products'))

@app.route('/products/edit/<int:pid>', methods=['POST'])
def edit_product(pid):
    p = Product.query.get_or_404(pid)
    p.name = request.form.get('name')
    p.sku = request.form.get('sku')
    p.price = float(request.form.get('price') or 0)
    p.quantity = int(request.form.get('quantity') or 0)
    p.reorder_level = int(request.form.get('reorder_level') or 0)
    supplier_id = request.form.get('supplier_id') or None
    if supplier_id:
        s = Supplier.query.get(int(supplier_id))
        if s:
            p.supplier = s
    else:
        p.supplier = None
    db.session.commit()
    flash('Product updated', 'success')
    return redirect(url_for('products'))

@app.route('/products/delete/<int:pid>', methods=['POST'])
def delete_product(pid):
    p = Product.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    flash('Product deleted', 'success')
    return redirect(url_for('products'))

# Suppliers CRUD
@app.route('/suppliers')
def suppliers():
    suppliers = Supplier.query.all()
    products = Product.query.all()
    return render_template('suppliers.html', suppliers=suppliers, products=products)

@app.route('/suppliers/add', methods=['POST'])
def add_supplier():
    name = request.form.get('name')
    contact = request.form.get('contact')
    if not name:
        flash('Supplier name required', 'danger')
        return redirect(url_for('suppliers'))
    s = Supplier(name=name, contact=contact)
    db.session.add(s)
    db.session.commit()
    flash('Supplier added', 'success')
    return redirect(url_for('suppliers'))

@app.route('/suppliers/associate', methods=['POST'])
def associate_product():
    supplier_id = int(request.form.get('supplier_id'))
    product_id = int(request.form.get('product_id'))
    s = Supplier.query.get_or_404(supplier_id)
    p = Product.query.get_or_404(product_id)
    p.supplier = s
    db.session.commit()
    flash('Product associated to supplier', 'success')
    return redirect(url_for('suppliers'))

# Transactions (purchase/sale)
@app.route('/transactions')
def transactions():
    txns = Transaction.query.order_by(Transaction.id.desc()).all()
    products = Product.query.all()
    return render_template('transactions.html', txns=txns, products=products)

@app.route('/transactions/add', methods=['POST'])
def add_transaction():
    product_id = int(request.form.get('product_id'))
    ttype = request.form.get('type')  # 'purchase' or 'sale'
    qty = int(request.form.get('quantity') or 0)
    product = Product.query.get_or_404(product_id)
    if ttype == 'sale' and qty > product.quantity:
        flash('Not enough stock for sale', 'danger')
        return redirect(url_for('transactions'))
    # update stock
    if ttype == 'purchase':
        product.quantity += qty
    else:
        product.quantity -= qty
    txn = Transaction(product_id=product.id, type=ttype, quantity=qty, unit_price=product.price)
    db.session.add(txn)
    db.session.commit()
    flash('Transaction recorded', 'success')
    return redirect(url_for('transactions'))

# Reports endpoints (JSON)
@app.route('/api/reports/low_stock')
def api_low_stock():
    items = Product.query.filter(Product.quantity <= Product.reorder_level).all()
    data = [{"id": p.id, "name": p.name, "quantity": p.quantity, "reorder_level": p.reorder_level} for p in items]
    return jsonify(data)

@app.route('/api/reports/inventory_value')
def api_inventory_value():
    total_value = db.session.query(func.sum(Product.quantity * Product.price)).scalar() or 0
    return jsonify({"total_value": total_value})

if __name__ == '__main__':
    app.run(debug=True)
