"""Flask Web Application for Warehouse Management"""
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from warehouse_manager import WarehouseManager

app = Flask(__name__)
app.secret_key = os.environ.get(
    'SECRET_KEY', 'dev-secret-key-change-in-production'
)

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
            success, message = manager.update_warehouse(
                warehouse_id, name, capacity, current_stock
            )
            if success:
                flash(message, 'success')
                return redirect(
                    url_for('view_warehouse', warehouse_id=warehouse_id)
                )
            return render_template('edit.html', warehouse=warehouse,
                                   error=message)
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
        amount_str = request.form.get('amount')
        if not amount_str:
            flash('Please enter an amount', 'error')
            return redirect(
                url_for('view_warehouse', warehouse_id=warehouse_id)
            )

        amount = float(amount_str)
        if amount <= 0:
            flash('Amount must be greater than zero', 'error')
            return redirect(
                url_for('view_warehouse', warehouse_id=warehouse_id)
            )

        if manager.add_to_warehouse(warehouse_id, amount):
            flash(f'Successfully added {amount:.2f} items', 'success')
        else:
            flash('Failed to add items', 'error')
    except ValueError:
        flash('Invalid amount format', 'error')
    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


@app.route('/warehouse/<int:warehouse_id>/remove', methods=['POST'])
def remove_from_warehouse(warehouse_id):
    """Remove items from a warehouse"""
    try:
        amount_str = request.form.get('amount')
        if not amount_str:
            flash('Please enter an amount', 'error')
            return redirect(
                url_for('view_warehouse', warehouse_id=warehouse_id)
            )

        amount = float(amount_str)
        if amount <= 0:
            flash('Amount must be greater than zero', 'error')
            return redirect(
                url_for('view_warehouse', warehouse_id=warehouse_id)
            )

        removed = manager.remove_from_warehouse(warehouse_id, amount)
        if removed > 0:
            flash(f'Successfully removed {removed:.2f} items', 'success')
        else:
            flash('Failed to remove items', 'error')
    except ValueError:
        flash('Invalid amount format', 'error')
    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


if __name__ == '__main__':
    # Debug mode should only be enabled in development
    debug_mode = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    app.run(debug=debug_mode)
