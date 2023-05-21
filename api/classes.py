class User:
    def __init__(self, username, password, is_active=True, role='client'):
        self.username = username
        self.password = password
        self.is_active = is_active
        self.role = role

class Category:
    def __init__(self, name):
        self.name = name

class Product:
    def __init__(self, name, amount_in_stock, price, in_stock=True):
        self.name = name
        self.amount_in_stock = amount_in_stock
        self.price = price
        self.in_stock = in_stock

    def to_dict(self):
        return {
            'name': self.name,
            'amount_in_stock': self.amount_in_stock,
            'price': self.price,
            'in_stock': self.in_stock
        }