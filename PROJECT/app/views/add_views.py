import requests
from flask import render_template, redirect, url_for
from flask.views import MethodView

from app import app, db
from app.form import AddEditOrderForm, AddEditClientForm, AddEditTourForm
from app.models import Client, Order, Tour
from app.tests.test_clients_api import BASE


# Add Views
class ControlOrderView(MethodView):
    def get(self):
        return render_template('add_edit_forms/add-edit_order.html', **self.prepare_context())

    def post(self):
        form = AddEditOrderForm()

        if form.validate_on_submit():
            requests.post(BASE + 'json_orders', data={
                'client_pass': form.client_pass.data.split()[0],
                'tour_date': form.tour_date.data,
                'tour_id': form.tour_id.data.split()[0],
                'days': form.days.data
            })

        return redirect(url_for('get_all_orders'))

    def prepare_context(self):
        form = AddEditOrderForm()

        clients = Client.query.all()
        form.client_pass.choices = list(
            f'{client.passport} - ({client.first_name} {client.last_name})' for client in clients
        )

        tours = Tour.query.all()
        form.tour_id.choices = list(
            f'{tour.id} - {tour.name}' for tour in tours
        )

        title = 'ADD ORDER'
        submit_url = '/add-order'
        cancel_button = 'get_all_orders'

        return {
            'title': title,
            'form': form,
            'submit_url': submit_url,
            'cancel_button': cancel_button
        }


class ControlClientView(MethodView):
    def get(self):
        return render_template('add_edit_forms/add-edit_client.html', **self.prepare_context())

    def post(self):
        form = AddEditClientForm()

        if form.validate_on_submit():
            requests.post(BASE + 'json_clients', data={
                'first_name': form.first_name.data,
                'last_name': form.second_name.data,
                'passport': form.passport.data,
                'email': form.email.data,
                'registration_date': form.register_date.data
            })

        return redirect(url_for('get_all_clients'))

    def prepare_context(self):
        form = AddEditClientForm()
        title = 'ADD CLIENT'
        submit_url = '/add-client'
        cancel_button = 'get_all_clients'

        return {
            'form': form,
            'title': title,
            'submit_url': submit_url,
            'cancel_button': cancel_button
        }


class ControlTourView(MethodView):
    def get(self):
        return render_template('add_edit_forms/add-edit_tour.html', **self.prepare_context())

    def post(self):
        form = AddEditTourForm()

        if form.validate_on_submit():
            requests.post(BASE + 'json_tours', data={
                'hotel': form.hotel_name.data,
                'name': form.tour_name.data,
                'day_cost': form.day_cost.data,
                'tour_includes': form.tour_includes.data,
                'country': form.country.data
            })

            return redirect(url_for('get_all_tours'))

    def prepare_context(self):
        form = AddEditTourForm()
        title = 'ADD TOUR'
        submit_url = '/add-tour'
        cancel_button = 'get_all_tours'

        return {
            'form': form,
            'title': title,
            'submit_url': submit_url,
            'cancel_button': cancel_button
        }


# End Add Views


app.add_url_rule('/add-order', view_func=ControlOrderView.as_view('add_order'), methods=['GET', 'POST'])
app.add_url_rule('/add-client', view_func=ControlClientView.as_view('add_client'), methods=['GET', 'POST'])
app.add_url_rule('/add-tour', view_func=ControlTourView.as_view('add_tour'), methods=['GET', 'POST'])
