"""Warehouse Manager - Manages multiple warehouses"""
from varasto import Varasto


class WarehouseManager:
    """Manages a collection of warehouses"""

    def __init__(self):
        self.warehouses = {}
        self.next_id = 1

    def create_warehouse(self, name, capacity, initial_stock=0):
        """Create a new warehouse with the given name and capacity"""
        warehouse_id = self.next_id
        self.next_id += 1
        self.warehouses[warehouse_id] = {
            'id': warehouse_id,
            'name': name,
            'varasto': Varasto(capacity, initial_stock)
        }
        return warehouse_id

    def get_warehouse(self, warehouse_id):
        """Get a warehouse by ID"""
        return self.warehouses.get(warehouse_id)

    def get_all_warehouses(self):
        """Get all warehouses"""
        return list(self.warehouses.values())

    def update_warehouse(self, warehouse_id, name, capacity, current_stock):
        """Update a warehouse's name and capacity"""
        if warehouse_id in self.warehouses:
            warehouse = self.warehouses[warehouse_id]
            warehouse['name'] = name
            # Create a new Varasto with updated values
            warehouse['varasto'] = Varasto(capacity, current_stock)
            return True
        return False

    def delete_warehouse(self, warehouse_id):
        """Delete a warehouse"""
        if warehouse_id in self.warehouses:
            del self.warehouses[warehouse_id]
            return True
        return False

    def add_to_warehouse(self, warehouse_id, amount):
        """Add items to a warehouse"""
        warehouse = self.get_warehouse(warehouse_id)
        if warehouse:
            warehouse['varasto'].lisaa_varastoon(amount)
            return True
        return False

    def remove_from_warehouse(self, warehouse_id, amount):
        """Remove items from a warehouse"""
        warehouse = self.get_warehouse(warehouse_id)
        if warehouse:
            return warehouse['varasto'].ota_varastosta(amount)
        return 0
