import requests
from flask import redirect, url_for
from flask.views import MethodView

from app import app, db

BASE = 'http://127.0.0.1:5000/'


# Delete Views
class DeleteTourView(MethodView):
    def post(self, id):
        requests.delete(BASE + 'json_tours/' + f'{id}')

        return redirect(url_for('get_all_tours'))


class DeleteOrderView(MethodView):
    def post(self, id):
        requests.delete(BASE + 'json_orders/' + f'{id}')

        return redirect(url_for('get_all_orders'))


class DeleteClientView(MethodView):
    def post(self, passport):
        requests.delete(BASE + 'json_clients/' + f'{passport}')

        return redirect(url_for('get_all_clients'))

# End Delete Views


app.add_url_rule('/delete-order/<int:id>', view_func=DeleteOrderView.as_view('delete_order'), methods=['POST'])
app.add_url_rule('/delete-client/<string:passport>', view_func=DeleteClientView.as_view('delete_client'),
                 methods=['POST'])
app.add_url_rule('/delete-tour/<int:id>', view_func=DeleteTourView.as_view('delete_tour'), methods=['POST'])
