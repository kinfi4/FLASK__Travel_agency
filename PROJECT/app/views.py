from flask import render_template
from flask.views import MethodView

from app import app
from app.form import AddEditOrderForm, AddEditClientForm, AddEditTourForm


class GetAllOrdersView(MethodView):
    def get(self):
        return render_template('tables/orders.html', **self.prepare_context())
    
    def prepare_context(self):
        title = 'Orders'
        add_button = 'add_order'
        return {
            'title': title,
            'add_button': add_button
        }


class GetAllClientsView(MethodView):
    def get(self):
        return render_template('tables/clients.html', **self.prepare_context())

    def prepare_context(self):
        title = 'Clients'
        add_button = 'add_client'
        return {
            'title': title,
            'add_button': add_button
        }


class GetAllToursView(MethodView):
    def get(self):
        return render_template('tables/tours.html', **self.prepare_context())

    def prepare_context(self):
        title = 'Tours'
        add_button = 'add_tour'
        return {
            'title': title,
            'add_button': add_button
        }


class AddOrderView(MethodView):
    def get(self):
        return render_template('add_edit_forms/add-edit_order.html', **self.prepare_context())

    def prepare_context(self):
        form = AddEditOrderForm()
        context = {
            'title': 'ADD ORDER',
            'form': form
        }

        return context


class AddClientView(MethodView):
    def get(self):
        return render_template('add_edit_forms/add-edit_client.html', form=AddEditClientForm(), title='ADD CLIENT')


class AddTourView(MethodView):
    def get(self):
        return render_template('add_edit_forms/add-edit_tour.html', form=AddEditTourForm(), title='ADD TOUR')


app.add_url_rule('/orders', view_func=GetAllOrdersView.as_view('get_all_orders'))
app.add_url_rule('/tours', view_func=GetAllToursView.as_view('get_all_tours'))
app.add_url_rule('/clients', view_func=GetAllClientsView.as_view('get_all_clients'))

app.add_url_rule('/add-order', view_func=AddOrderView.as_view('add_order'))
app.add_url_rule('/add-client', view_func=AddClientView.as_view('add_client'))
app.add_url_rule('/add-tour', view_func=AddTourView.as_view('add_tour'))
