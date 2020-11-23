from flask import render_template, redirect, request, url_for
from flask.views import MethodView

from app import app, db
from app.form import AddEditOrderForm, AddEditClientForm, AddEditTourForm

from app.models import Client, Order, Tour


class GetAllOrdersView(MethodView):
    def get(self):
        return render_template('tables/orders.html', **self.prepare_context())
    
    def prepare_context(self):
        title = 'Orders'
        add_button = 'add_order'
        orders = Order.query.all()

        return {
            'title': title,
            'add_button': add_button,
            'orders': orders
        }


class GetAllClientsView(MethodView):
    def get(self):
        return render_template('tables/clients.html', **self.prepare_context())

    def prepare_context(self):
        title = 'Clients'
        add_button = 'add_client'
        clients = Client.query.all()

        return {
            'title': title,
            'add_button': add_button,
            'clients': clients
        }


class GetAllToursView(MethodView):
    def get(self):
        return render_template('tables/tours.html', **self.prepare_context())

    def prepare_context(self):
        title = 'Tours'
        add_button = 'add_tour'
        tours = Tour.query.all()

        return {
            'title': title,
            'add_button': add_button,
            'tours': tours
        }


class AddOrderView(MethodView):
    def get(self):
        return render_template('add_edit_forms/add-edit_order.html', **self.prepare_context())

    def prepare_context(self):
        form = AddEditOrderForm()
        title = 'ADD ORDER'
        submit_url = '/add-order'

        return {
            'title': title,
            'form': form,
            'submit_url': submit_url
        }


class AddClientView(MethodView):
    def get(self):
        return render_template('add_edit_forms/add-edit_client.html', form=AddEditClientForm(), title='ADD CLIENT')

    def post(self):
        form = AddEditClientForm()

        client = Client()
        client.first_name = form.first_name.data
        client.last_name = form.second_name.data
        client.passport = form.passport.data
        client.registration_date = form.register_date.data

        db.session.add(client)
        db.session.commit()

        return redirect(url_for('get_all_clients'))

    def prepare_context(self):
        form = AddEditClientForm()
        title = 'ADD CLIENT'
        submit_url = '/add-client'

        return {
            'form': form,
            'title': title,
            'submit_url': submit_url
        }


class AddTourView(MethodView):
    def get(self):
        return render_template('add_edit_forms/add-edit_tour.html', **self.prepare_context())

    def post(self):
        form = AddEditTourForm()

    def prepare_context(self):
        form = AddEditTourForm()
        title = 'ADD TOUR'
        submit_url = '/add-tour'

        return {
            'form': form,
            'title': title,
            'submit_url': submit_url
        }


app.add_url_rule('/orders', view_func=GetAllOrdersView.as_view('get_all_orders'))
app.add_url_rule('/tours', view_func=GetAllToursView.as_view('get_all_tours'))
app.add_url_rule('/clients', view_func=GetAllClientsView.as_view('get_all_clients'))

app.add_url_rule('/add-order', view_func=AddOrderView.as_view('add_order'))
app.add_url_rule('/add-client', view_func=AddClientView.as_view('add_client'))
app.add_url_rule('/add-tour', view_func=AddTourView.as_view('add_tour'))
