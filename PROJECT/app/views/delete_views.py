from flask import redirect, url_for
from flask.views import MethodView

from app import app, db
from app.models import Client, Order, Tour


# Delete Views
class DeleteTourView(MethodView):
    def post(self, id):
        tour = Tour.query.get(id)

        db.session.delete(tour)
        db.session.commit()

        return redirect(url_for('get_all_tours'))


class DeleteOrderView(MethodView):
    def post(self, id):
        order = Order.query.get(id)

        db.session.delete(order)
        db.session.commit()

        return redirect(url_for('get_all_orders'))


class DeleteClientView(MethodView):
    def post(self, passport):
        client = Client.query.get(passport)

        db.session.delete(client)
        db.session.commit()

        return redirect(url_for('get_all_clients'))

# End Delete Views


app.add_url_rule('/delete-order/<int:id>', view_func=DeleteOrderView.as_view('delete_order'), methods=['POST'])
app.add_url_rule('/delete-client/<string:passport>', view_func=DeleteClientView.as_view('delete_client'),
                 methods=['POST'])
app.add_url_rule('/delete-tour/<int:id>', view_func=DeleteTourView.as_view('delete_tour'), methods=['POST'])
