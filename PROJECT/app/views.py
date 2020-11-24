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


# Add Views
class ControlOrderView(MethodView):
    def get(self):
        return render_template('add_edit_forms/add-edit_order.html', **self.prepare_context())

    def post(self):
        form = AddEditOrderForm()

        print(form.client_pass.data.split()[0])
        print(form.tour_id.data.split()[0])

        # if form.validate_on_submit():
        order = Order()

        order.client_pass = form.client_pass.data.split()[0]
        order.add_date = form.add_date.data
        order.tour_id = form.tour_id.data.split()[0]
        order.days = form.days.data

        db.session.add(order)
        db.session.commit()

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
        client = Client()

        if form.validate_on_submit():
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
            tour = Tour()
            tour.hotel = form.hotel_name.data
            tour.name = form.tour_name.data
            tour.day_cost = form.day_cost.data
            tour.tour_includes = form.tour_includes.data
            tour.country = form.country.data

            db.session.add(tour)
            db.session.commit()

            return redirect(url_for('get_all_tours'))

    def delete(self, id):
        tour = Tour.query.get(id)

        db.session.delete(tour)
        db.session.commit()

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
        if form.validate_on_submit():
            order.add_date = form.add_date.data
            order.tour_id = form.tour_id.data.split()[0]
            order.client_pass = form.client_pass.data.split()[0]
            order.days = form.days.data

            db.session.commit()

        return redirect(url_for('get_all_tours'))

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
        form.add_date.data = order.add_date

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

            db.session.commit()

        return redirect(url_for('get_all_clients'))

    def prepare_context(self, client):
        form = AddEditClientForm()

        form.first_name.data = client.first_name
        form.second_name.data = client.last_name
        form.passport.data = client.passport
        form.register_date.data = client.registration_date

        submit_url = '/edit-client/' + str(client.passport)
        cancel_button = 'get_all_clients'

        return {
            'form': form,
            'title': 'EDIT CLIENT',
            'submit_url': submit_url,
            'cancel_button': cancel_button
        }


app.add_url_rule('/orders', view_func=GetAllOrdersView.as_view('get_all_orders'))
app.add_url_rule('/clients', view_func=GetAllClientsView.as_view('get_all_clients'))
app.add_url_rule('/tours', view_func=GetAllToursView.as_view('get_all_tours'))

app.add_url_rule('/add-order', view_func=ControlOrderView.as_view('add_order'), methods=['GET', 'POST'])
app.add_url_rule('/add-client', view_func=ControlClientView.as_view('add_client'), methods=['GET', 'POST'])
app.add_url_rule('/add-tour', view_func=ControlTourView.as_view('add_tour'), methods=['GET', 'POST'])

app.add_url_rule('/delete-order/<int:id>', view_func=DeleteOrderView.as_view('delete_order'), methods=['POST'])
app.add_url_rule('/delete-client/<string:passport>', view_func=DeleteClientView.as_view('delete_client'),
                 methods=['POST'])
app.add_url_rule('/delete-tour/<int:id>', view_func=DeleteTourView.as_view('delete_tour'), methods=['POST'])

app.add_url_rule('/edit-tour/<int:id>', view_func=EditTourView.as_view('edit_tour'), methods=['POST', 'GET'])
app.add_url_rule('/edit-order/<int:id>', view_func=EditOrderView.as_view('edit_order'), methods=['POST', 'GET'])
app.add_url_rule('/edit-client/<string:passport>', view_func=EditClientView.as_view('edit_client'), methods=['POST', 'GET'])