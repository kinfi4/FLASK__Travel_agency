from flask import render_template

from app import app


@app.route('/orders')
def get_all_orders():
    print('hello world')
    return render_template('orders.html')


