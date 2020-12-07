from flask import render_template, redirect, url_for
from flask.views import MethodView

from app.form import AddEditTourForm, AddEditClientForm, AddEditOrderForm
from app import app, db
from app.models import Client, Order, Tour


# Edit Views
class EditTourView(MethodView):
    def get(self, id):
        try:
            tour = Tour.query.get(id)
        except:
            return redirect(url_for('get_all_tours'))

        return render_template('add_edit_forms/add-edit_tour.html', **self.prepare_context(tour))

    def post(self, id):
        try:
            tour = Tour.query.get(id)
        except:
            return redirect(url_for('get_all_tours'))

        form = AddEditTourForm()
        if form.validate_on_submit():
            tour.hotel = form.hotel_name.data
            tour.name = form.tour_name.data
            tour.day_cost = form.day_cost.data
            tour.tour_includes = form.tour_includes.data
            tour.country = form.country.data

            db.session.commit()

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
        try:
            order = Order.query.get(id)
        except:
            return redirect(url_for('get_all_orders'))

        return render_template('add_edit_forms/add-edit_order.html', **self.prepare_context(order))

    def post(self, id):
        try:
            order = Order.query.get(id)
        except:
            return redirect(url_for('get_all_orders'))

        form = AddEditOrderForm()

        print(form.validate_on_submit())
        print(form.errors)

        if form.validate_on_submit():
            order.tour_date = form.tour_date.data
            order.tour_id = form.tour_id.data.split()[0]
            order.client_pass = form.client_pass.data.split()[0]
            order.days = form.days.data

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
        try:
            client = Client.query.get(passport)
        except:
            return redirect(url_for('get_all_clients'))

        return render_template('add_edit_forms/add-edit_client.html', **self.prepare_context(client))

    def post(self, passport):
        try:
            client = Client.query.get(passport)
        except:
            return redirect(url_for('get_all_clients'))

        form = AddEditClientForm()
        if form.validate_on_submit():
            client.first_name = form.first_name.data
            client.last_name = form.second_name.data
            client.passport = form.passport.data
            client.registration_date = form.register_date.data
            client.email = form.email.data

            db.session.commit()

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
