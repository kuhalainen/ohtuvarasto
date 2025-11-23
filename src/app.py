"""Flask Web Application for Warehouse Management"""
from flask import Flask, render_template, request, redirect, url_for
from warehouse_manager import WarehouseManager

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-in-production'

# Initialize the warehouse manager
manager = WarehouseManager()


@app.route('/')
def index():
    """Show all warehouses"""
    warehouses = manager.get_all_warehouses()
    return render_template('index.html', warehouses=warehouses)


@app.route('/warehouse/create', methods=['GET', 'POST'])
def create_warehouse():
    """Create a new warehouse"""
    if request.method == 'POST':
        name = request.form.get('name', '')
        try:
            capacity = float(request.form.get('capacity', 0))
            initial_stock = float(request.form.get('initial_stock', 0))
            manager.create_warehouse(name, capacity, initial_stock)
            return redirect(url_for('index'))
        except ValueError:
            return render_template('create.html', error="Invalid number format")

    return render_template('create.html')


@app.route('/warehouse/<int:warehouse_id>')
def view_warehouse(warehouse_id):
    """View a specific warehouse"""
    warehouse = manager.get_warehouse(warehouse_id)
    if not warehouse:
        return redirect(url_for('index'))
    return render_template('view.html', warehouse=warehouse)


@app.route('/warehouse/<int:warehouse_id>/edit', methods=['GET', 'POST'])
def edit_warehouse(warehouse_id):
    """Edit a warehouse"""
    warehouse = manager.get_warehouse(warehouse_id)
    if not warehouse:
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name', '')
        try:
            capacity = float(request.form.get('capacity', 0))
            current_stock = float(request.form.get('current_stock', 0))
            manager.update_warehouse(
                warehouse_id, name, capacity, current_stock
            )
            return redirect(
                url_for('view_warehouse', warehouse_id=warehouse_id)
            )
        except ValueError:
            return render_template('edit.html', warehouse=warehouse,
                                   error="Invalid number format")

    return render_template('edit.html', warehouse=warehouse)


@app.route('/warehouse/<int:warehouse_id>/delete', methods=['POST'])
def delete_warehouse(warehouse_id):
    """Delete a warehouse"""
    manager.delete_warehouse(warehouse_id)
    return redirect(url_for('index'))


@app.route('/warehouse/<int:warehouse_id>/add', methods=['POST'])
def add_to_warehouse(warehouse_id):
    """Add items to a warehouse"""
    try:
        amount = float(request.form.get('amount', 0))
        manager.add_to_warehouse(warehouse_id, amount)
    except ValueError:
        pass
    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


@app.route('/warehouse/<int:warehouse_id>/remove', methods=['POST'])
def remove_from_warehouse(warehouse_id):
    """Remove items from a warehouse"""
    try:
        amount = float(request.form.get('amount', 0))
        manager.remove_from_warehouse(warehouse_id, amount)
    except ValueError:
        pass
    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


if __name__ == '__main__':
    app.run(debug=True)
