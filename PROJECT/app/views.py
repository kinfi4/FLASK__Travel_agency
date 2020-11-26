from datetime import date

from flask import render_template, redirect, request, url_for
from flask.views import MethodView
from sqlalchemy import func

from app import app, db
from app.form import AddEditOrderForm, AddEditClientForm, AddEditTourForm
from app.models import Client, Order, Tour


# Get All Entities
class GetAllOrdersView(MethodView):
    def get(self):
        return render_template('tables/orders.html', **self.prepare_context(request.args))

    def prepare_context(self, filters=None):
        title = 'Orders'
        add_button = 'add_order'

        if filters:
            s_from_date = filters['tour_date_from']
            s_by_date = filters['tour_date_by']

            if s_from_date and s_by_date:
                from_date = date.fromisoformat(s_from_date)
                by_date = date.fromisoformat(s_by_date)

                by_date.replace(by_date.year, by_date.month, by_date.day + 1)
                from_date.replace(from_date.year, from_date.month, from_date.day - 1)

                orders = Order.query.filter(Order.tour_date > from_date).filter(by_date > Order.tour_date)
            elif s_from_date:
                from_date = date.fromisoformat(s_from_date)
                from_date.replace(from_date.year, from_date.month, from_date.day - 1)

                orders = Order.query.filter(Order.tour_date >= from_date)
            elif s_by_date:
                by_date = date.fromisoformat(s_by_date)
                by_date.replace(by_date.year, by_date.month, by_date.day + 1)

                orders = Order.query.filter(by_date >= Order.tour_date)
            else:
                orders = Order.query.all()
        else:
            orders = Order.query.all()

        return {
            'title': title,
            'add_button': add_button,
            'orders': orders,
            'sort_from': filters.get('tour_date_from', None),
            'sort_by': filters.get('tour_date_by', None)
        }


class GetAllClientsView(MethodView):
    def get(self):
        return render_template('tables/clients.html', **self.prepare_context(request.args))

    def prepare_context(self, filters=None):
        title = 'Clients'
        add_button = 'add_client'

        if filters:
            s_from_date = filters['tour_date_from']
            s_by_date = filters['tour_date_by']

            if s_from_date and s_by_date:
                from_date = date.fromisoformat(s_from_date)
                by_date = date.fromisoformat(s_by_date)

                by_date.replace(by_date.year, by_date.month, by_date.day + 1)
                from_date.replace(from_date.year, from_date.month, from_date.day - 1)

                clients = Client.query.filter(Client.registration_date > from_date).filter(
                    by_date > Client.registration_date)
            elif s_from_date:
                from_date = date.fromisoformat(s_from_date)
                from_date.replace(from_date.year, from_date.month, from_date.day - 1)

                clients = Client.query.filter(Client.registration_date >= from_date)
            elif s_by_date:
                by_date = date.fromisoformat(s_by_date)
                by_date.replace(by_date.year, by_date.month, by_date.day + 1)

                clients = Client.query.filter(by_date >= Client.registration_date)
            else:
                clients = Client.query.all()
        else:
            clients = Client.query.all()

        return {
            'title': title,
            'add_button': add_button,
            'clients': clients,
            'sort_from': filters.get('tour_date_from', None),
            'sort_by': filters.get('tour_date_by', None)
        }


class GetAllToursView(MethodView):
    def get(self):
        return render_template('tables/tours.html', **self.prepare_context(request.args))

    def prepare_context(self, filters=None):
        title = 'Tours'
        add_button = 'add_tour'

        if filters:
            from_price = float(filters['from_price'])
            by_price = float(filters['by_price'])

            if from_price and by_price:
                tours = Tour.query.filter(Tour.day_cost > int(from_price)).filter(by_price > Tour.day_cost)
            elif from_price:
                tours = Tour.query.filter(Tour.day_cost >= from_price)
            elif by_price:
                tours = Tour.query.filter(by_price >= Tour.day_cost)
            else:
                tours = Tour.query.all()
        else:
            tours = Tour.query.all()

        return {
            'title': title,
            'add_button': add_button,
            'tours': tours,
            'from_price': filters.get('from_price', None),
            'by_price': filters.get('by_price', None)
        }
# End Get All Entities


# Add Views
class ControlOrderView(MethodView):
    def get(self):
        return render_template('add_edit_forms/add-edit_order.html', **self.prepare_context())

    def post(self):
        form = AddEditOrderForm()

        print(form.client_pass.data.split()[0])
        print(form.tour_id.data.split()[0])

        if form.validate_on_submit():
            order = Order()

            order.client_pass = form.client_pass.data.split()[0]
            order.tour_date = form.tour_date.data
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
            client.email = form.email.data
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


app.add_url_rule('/orders', view_func=GetAllOrdersView.as_view('get_all_orders'), methods=['GET', 'POST'])
app.add_url_rule('/clients', view_func=GetAllClientsView.as_view('get_all_clients'), methods=['GET', 'POST'])
app.add_url_rule('/tours', view_func=GetAllToursView.as_view('get_all_tours'), methods=['GET', 'POST'])

app.add_url_rule('/add-order', view_func=ControlOrderView.as_view('add_order'), methods=['GET', 'POST'])
app.add_url_rule('/add-client', view_func=ControlClientView.as_view('add_client'), methods=['GET', 'POST'])
app.add_url_rule('/add-tour', view_func=ControlTourView.as_view('add_tour'), methods=['GET', 'POST'])

app.add_url_rule('/delete-order/<int:id>', view_func=DeleteOrderView.as_view('delete_order'), methods=['POST'])
app.add_url_rule('/delete-client/<string:passport>', view_func=DeleteClientView.as_view('delete_client'),
                 methods=['POST'])
app.add_url_rule('/delete-tour/<int:id>', view_func=DeleteTourView.as_view('delete_tour'), methods=['POST'])

app.add_url_rule('/edit-tour/<int:id>', view_func=EditTourView.as_view('edit_tour'), methods=['POST', 'GET'])
app.add_url_rule('/edit-order/<int:id>', view_func=EditOrderView.as_view('edit_order'), methods=['POST', 'GET'])
app.add_url_rule('/edit-client/<string:passport>', view_func=EditClientView.as_view('edit_client'),
                 methods=['POST', 'GET'])
