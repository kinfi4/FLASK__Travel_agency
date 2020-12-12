import requests
from flask import render_template, redirect, url_for, abort
from flask.views import MethodView

from app.form import AddEditTourForm, AddEditClientForm, AddEditOrderForm
from app import app, db
from app.models import Client, Order, Tour
from app.tests.test_clients_api import BASE


# Edit Views
class EditTourView(MethodView):
    def get(self, id):
        tour = Tour.query.get(id)
        if not tour:
            abort(404)

        return render_template('add_edit_forms/add-edit_tour.html', **self.prepare_context(tour))

    def post(self, id):
        if not Tour.query.get(id):
            abort(404)

        form = AddEditTourForm()
        if form.validate_on_submit():
            requests.put(BASE + 'json_tours/' + str(id), data={
                'hotel': form.hotel_name.data,
                'name': form.tour_name.data,
                'day_cost': form.day_cost.data,
                'tour_includes': form.tour_includes.data,
                'country': form.country.data
            })

        return redirect(url_for('get_all_tours'))

    def prepare_context(self, tour):
        form = AddEditTourForm()
        form.country.data = tour.country
        form.tour_name.data = tour.name
        form.hotel_name.data = tour.hotel
        form.day_cost.data = tour.day_cost
        form.country.data = tour.country
        form.tour_includes.data = tour.tour_includes

        submit_url = '/edit-tour/' + str(tour.id)
        cancel_button = 'get_all_tours'

        return {
            'form': form,
            'title': 'EDIT TOUR',
            'submit_url': submit_url,
            'cancel_button': cancel_button
        }


class EditOrderView(MethodView):
    def get(self, id):
        order = Order.query.get(id)
        if not order:
            abort(404)

        return render_template('add_edit_forms/add-edit_order.html', **self.prepare_context(order))

    def post(self, id):
        if not Order.query.get(id):
            abort(404)

        form = AddEditOrderForm()
        if form.validate_on_submit():
            requests.put(BASE + 'json_orders/' + str(id), data={
                'client_pass': form.client_pass.data.split()[0],
                'tour_date': form.tour_date.data,
                'tour_id': form.tour_id.data.split()[0],
                'days': form.days.data
            })

            db.session.commit()

        return redirect(url_for('get_all_orders'))

    def prepare_context(self, order):
        form = AddEditOrderForm()

        clients = Client.query.all()
        order_client = Client.query.get(order.client_pass)
        form.client_pass.choices = [f'{order_client.passport} - {order_client.first_name} {order_client.last_name}'] \
                                   + list(
            f'{client.passport} - ({client.first_name} {client.last_name})' for client in clients if
            client != order_client
        )

        tours = Tour.query.all()
        order_tour = Tour.query.get(order.tour_id)
        form.tour_id.choices = [f'{order_tour.id} - {order_tour.name}'] + list(
            f'{tour.id} - {tour.name}' for tour in tours if tour != order_tour
        )

        form.days.data = order.days
        form.tour_date.data = order.tour_date

        submit_url = '/edit-order/' + str(order.id)
        cancel_button = 'get_all_orders'

        return {
            'form': form,
            'title': 'EDIT ORDER',
            'submit_url': submit_url,
            'cancel_button': cancel_button
        }


class EditClientView(MethodView):
    def get(self, passport):
        client = Client.query.get(passport)
        if not client:
            abort(404)

        return render_template('add_edit_forms/add-edit_client.html', **self.prepare_context(client))

    def post(self, passport):
        if not Client.query.get(passport):
            abort(404)

        form = AddEditClientForm()
        if form.validate_on_submit():
            requests.put(BASE + 'json_clients/' + str(passport), data={
                'first_name': form.first_name.data,
                'last_name': form.second_name.data,
                'passport': form.passport.data,
                'email': form.email.data,
                'registration_date': form.register_date.data
            })

        return redirect(url_for('get_all_clients'))

    def prepare_context(self, client):
        form = AddEditClientForm()

        form.first_name.data = client.first_name
        form.second_name.data = client.last_name
        form.passport.data = client.passport
        form.register_date.data = client.registration_date
        form.email.data = client.email

        submit_url = '/edit-client/' + str(client.passport)
        cancel_button = 'get_all_clients'

        return {
            'form': form,
            'title': 'EDIT CLIENT',
            'submit_url': submit_url,
            'cancel_button': cancel_button
        }
# End Edit Views


app.add_url_rule('/edit-tour/<int:id>', view_func=EditTourView.as_view('edit_tour'), methods=['POST', 'GET'])
app.add_url_rule('/edit-order/<int:id>', view_func=EditOrderView.as_view('edit_order'), methods=['POST', 'GET'])
app.add_url_rule('/edit-client/<string:passport>', view_func=EditClientView.as_view('edit_client'),
                 methods=['POST', 'GET'])
