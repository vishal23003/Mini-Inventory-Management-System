from models import db, Product, Supplier, Transaction
from app import app
import random

with app.app_context():
    # Add suppliers
    s1 = Supplier(name='Alpha Traders', contact='alpha@example.com')
    s2 = Supplier(name='Beta Wholesale', contact='beta@example.com')
    db.session.add_all([s1, s2])
    db.session.commit()

    # Add products
    p1 = Product(name='Notebook A5', sku='NB-A5', price=45.0, quantity=50, reorder_level=10, supplier=s1)
    p2 = Product(name='Ballpoint Pen', sku='BP-01', price=12.5, quantity=200, reorder_level=50, supplier=s2)
    p3 = Product(name='Stapler', sku='ST-01', price=150.0, quantity=5, reorder_level=10, supplier=s1)
    db.session.add_all([p1, p2, p3])
    db.session.commit()

    # Sample transactions
    t1 = Transaction(product_id=p2.id, type='sale', quantity=5, unit_price=p2.price)
    t2 = Transaction(product_id=p3.id, type='purchase', quantity=20, unit_price=p3.price)
    db.session.add_all([t1, t2])
    db.session.commit()
    print('Sample data added')
