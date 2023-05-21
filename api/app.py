from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from wtforms import Form, StringField, PasswordField, SelectField, IntegerField, BooleanField, FloatField
from wtforms.validators import InputRequired, EqualTo, NumberRange
from bson.objectid import ObjectId
import requests
import functools
import jwt
from datetime import datetime, timedelta


# Config System
app = Flask(__name__)
CORS(app)
client = MongoClient('mongodb://localhost:27017')
db = client['online_store']
user_collection = db['users']
category_collection = db['categories']
product_collection = db['products']
cart_collection = db['carts']

#Generate Token 
def generate_jwt_token(user_id):
    payload = {'user_id': user_id}
    token = jwt.encode(payload, 'secret_key', algorithm='HS256')
    return token

#Client Login Decorator
def require_login(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        user_id = request.headers.get('User-ID')  # Assuming user ID is provided in the request headers
        user = user_collection.find_one({'id': int(user_id)})
        if user and user['is_active']:
            return view(*args, **kwargs)
        else:
            return jsonify({'error': 'Unauthorized or inactive user'}), 401
    return wrapped_view

#Admin Login Decorator
def require_admin(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        user_id = request.headers.get('User-ID')  # Assuming user ID is provided in the request headers
        if user_id is None:
            return jsonify({'error': 'User-ID header is missing'}), 400

        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({'error': 'User-ID must be a valid integer'}), 400

        user = user_collection.find_one({'id': user_id})
        if user and user['is_active'] and user['role'] == 'admin':
            return view(*args, **kwargs)
        else:
            return jsonify({'error': 'Unauthorized or inactive user or not an admin'}), 401

    return wrapped_view



class UserForm(Form):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired()])
    is_active = SelectField('Is Active', choices=[('true', 'True'), ('false', 'False')], default='true')
    role = SelectField('Role', choices=[('admin', 'Admin'), ('client', 'Client')], default='client')

class CategoryForm(Form):
    name = StringField('Name', validators=[InputRequired()])

class ProductForm(Form):
    name = StringField('Name', validators=[InputRequired()])
    amount_in_stock = IntegerField('Amount in Stock', validators=[InputRequired(), NumberRange(min=0)])
    price = FloatField('Price', validators=[InputRequired(), NumberRange(min=0)])
    in_stock = BooleanField('In Stock', default=True)
    category_id = StringField('Category ID')

class Cart:
    def __init__(self, user_id):
        self.user_id = user_id
        self.items = []

    def add_to_cart(self, product_id, quantity):
        self.items.append({'product_id': product_id, 'quantity': quantity})

    def remove_from_cart(self, product_id):
        for item in self.items:
            if item['product_id'] == product_id:
                self.items.remove(item)
                break

    def get_cart_items(self):
        return self.items

#-------USER------- 
#-------Create an User------- 
@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.form
    form = UserForm(user_data)
    if form.validate():
        user_id = int(user_collection.count_documents({}) + 1)
        user = {
            '_id': str(ObjectId()),  # Generate a unique MongoDB ObjectId as the _id field
            'id': user_id,  # Store the user ID separately
            'username': form.username.data,
            'password': form.password.data,
            'is_active': form.is_active.data == 'true',
            'role': form.role.data
        }
        user_collection.insert_one(user)
        return jsonify({'message': 'User created successfully', 'id': user_id}), 201
    return jsonify({'error': 'Validation failed', 'validation_errors': form.errors}), 400

#-------Get All Users------- 
@app.route('/users', methods=['GET'])
def get_users():
    users = list(user_collection.find({}, {'_id': 0}))
    return jsonify(users)

#-------Get an User------- 
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = user_collection.find_one({'id': int(user_id)}, {'_id': 0})
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

#-------Update an User------- 
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.form
    form = UserForm(user_data)
    if form.validate():
        result = user_collection.update_one({'id': int(user_id)}, {'$set': {
            'username': form.username.data,
            'password': form.password.data,
            'is_active': form.is_active.data == 'true',
            'role': form.role.data
        }})
        if result.modified_count > 0:
            return jsonify({'message': 'User updated successfully'})
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'error': 'Validation failed', 'validation_errors': form.errors}), 400

#-------Delete an User------- 
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = user_collection.delete_one({'id': int(user_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'error': 'User not found'}), 404

#-------Login an User------- 
@app.route('/login', methods=['POST'])
def login():
    login_data = request.get_json()
    username = login_data.get('username')
    password = login_data.get('password')

    user = user_collection.find_one({'username': username})
    if user and user['password'] == password:
        if not user['is_active']:
            return jsonify({'error': 'Inactive user'}), 403

        # Generate authentication token
        token = generate_jwt_token(user['id'])

        return jsonify({'message': 'Login successful', 'role': user['role'], 'token': token})
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


#-------Activate User------- 
@app.route('/users/<user_id>/activate', methods=['PUT'])
def activate_user(user_id):
    result = user_collection.update_one({'id': int(user_id)}, {'$set': {'is_active': True}})
    if result.modified_count > 0:
        return jsonify({'message': 'User activated successfully'})
    return jsonify({'error': 'User not found'}), 404

#-------Deactivate User------- 
@app.route('/users/<user_id>/deactivate', methods=['PUT'])
@require_admin
def deactivate_user(user_id):
    result = user_collection.update_one({'id': int(user_id)}, {'$set': {'is_active': False}})
    if result.modified_count > 0:
        return jsonify({'message': 'User deactivated successfully'})
    return jsonify({'error': 'User not found'}), 404



#-------CATEGORY------- 
#-------create category------- 
@app.route('/categories', methods=['POST'])
@require_admin
def create_category():
    category_data = request.get_json()
    name = category_data.get('name')
    if name:
        category = {'name': name}
        result = category_collection.insert_one(category)
        category_id = str(result.inserted_id)
        return jsonify({'message': 'Category created successfully', 'id': category_id}), 201
    else:
        return jsonify({'error': 'Category name is missing'}), 400


#-------update category------- 
@app.route('/categories/<category_id>', methods=['PUT'])
@require_admin
def update_category(category_id):
    category_data = request.json
    if 'name' not in category_data:
        return jsonify({'error': 'Name field is required'}), 400

    name = category_data['name']

    # Perform the category update operation
    result = category_collection.update_one({'_id': ObjectId(category_id)}, {'$set': {'name': name}})
    if result.modified_count > 0:
        return jsonify({'message': 'Category updated successfully'})
    return jsonify({'error': 'Category not found'}), 404

#-------delete category------- 
@app.route('/categories/<category_id>', methods=['DELETE'])
@require_admin
def delete_category(category_id):
    result = category_collection.delete_one({'_id': ObjectId(category_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'Category deleted successfully'})
    return jsonify({'error': 'Category not found'}), 404


#-------PRODUCT------- 
#-------Create Product------- 

@app.route('/products', methods=['POST'])
@require_admin
def create_product():
    product_data = request.form
    form = ProductForm(product_data)
    if form.validate():
        product_id = str(product_collection.count_documents({}) + 1)
        category_id = request.form.get('category_id')  # Get category id from request form
        product = {
            'id': product_id,
            'name': form.name.data,
            'amount_in_stock': form.amount_in_stock.data,
            'price': form.price.data,
            'in_stock': form.in_stock.data,
            'category_id': category_id  # Add category_id to product data
        }
        product_collection.insert_one(product)
        return jsonify({'message': 'Product created successfully', 'id': product_id}), 201
    return jsonify({'error': 'Validation failed', 'validation_errors': form.errors}), 400

#------- Get All Products-------
@app.route('/products', methods=['GET'])
def get_all_products():
    products = list(product_collection.find({'amount_in_stock': {'$gt': 0}}, {'_id': 0}))
    return jsonify(products)

#-------Get a Product-------
@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = product_collection.find_one({'_id': ObjectId(product_id), 'amount_in_stock': {'$gt': 0}}, {'_id': 0})
    if product:
        return jsonify(product)
    return jsonify({'error': 'Product not found or amount_in_stock is 0'}), 404


#------- Update a Product------- 
@app.route('/products/<product_id>', methods=['PUT'])
@require_admin
def update_product(product_id):
    product_data = request.json
    if 'name' not in product_data:
        return jsonify({'error': 'Name field is required'}), 400
    if 'price' not in product_data:
        return jsonify({'error': 'Price field is required'}), 400
    if 'amount_in_stock' not in product_data:
        return jsonify({'error': 'Amount in stock field is required'}), 400

    name = product_data['name']
    price = product_data['price']
    amount_in_stock = product_data['amount_in_stock']

    # Update Product
    result = product_collection.update_one({'_id': ObjectId(product_id)}, {'$set': {'name': name, 'price': price, 'amount_in_stock': amount_in_stock}})
    if result.modified_count > 0:
        return jsonify({'message': 'Product updated successfully'})
    return jsonify({'error': 'Product not found'}), 404


#-------Delete a Product------- 
@app.route('/products/<product_id>', methods=['DELETE'])
@require_admin
def delete_product(product_id):
    result = product_collection.delete_one({'_id': ObjectId(product_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'Product deleted successfully'})
    return jsonify({'error': 'Product not found'}), 404

#-------Get Products by Category------- 
@app.route('/products_by_category/<category_id>', methods=['GET'])
def get_products_by_category(category_id):
    products = list(product_collection.find({'category_id': category_id}, {'_id': 0}))
    return jsonify(products)

#-------CART-------
#-------Add a Product to Cart-------
@app.route('/cart/add', methods=['POST'])
@require_login
def add_to_cart():
    cart_data = request.json
    user_id = cart_data.get('user_id')
    product_id = cart_data.get('product_id')
    quantity = cart_data.get('quantity')

    if not user_id or not product_id or not quantity:
        return jsonify({'error': 'User ID, product ID, and quantity are required'}), 400

    cart = Cart(user_id)
    cart.add_to_cart(product_id, quantity)

    # Calculate total price
    total_price = 0.0
    for item in cart.get_cart_items():
        product = product_collection.find_one({'_id': ObjectId(item['product_id'])})
        if product:
            total_price += product['price'] * item['quantity']

    # Save cart in the database
    cart_data = {
        'user_id': user_id,
        'items': cart.get_cart_items(),
        'count': len(cart.get_cart_items()),
        'total_price': total_price
    }
    cart_collection.insert_one(cart_data)

    return jsonify({'message': 'Item added to cart successfully'})

#-------Remove a Product From a Cart-------
@app.route('/cart/remove', methods=['POST'])
@require_login
def remove_from_cart():
    cart_data = request.json
    user_id = cart_data.get('user_id')
    product_id = cart_data.get('product_id')

    if not user_id or not product_id:
        return jsonify({'error': 'User ID and product ID are required'}), 400

    cart = Cart(user_id)
    cart.remove_from_cart(product_id)

    # Calculate total price
    total_price = 0.0
    for item in cart.get_cart_items():
        product = product_collection.find_one({'_id': ObjectId(item['product_id'])})
        if product:
            total_price += product['price'] * item['quantity']

    # Save cart in the database
    cart_data = {
        'user_id': user_id,
        'items': cart.get_cart_items(),
        'count': len(cart.get_cart_items()),
        'total_price': total_price
    }
    cart_collection.insert_one(cart_data)

    return jsonify({'message': 'Item removed from cart successfully'})

#------- Get an User's Cart-------
@app.route('/cart/<user_id>', methods=['GET'])
def get_user_cart(user_id):
    cart = cart_collection.find_one({'user_id': user_id})
    if cart:
        cart['_id'] = str(cart['_id'])  # Convert ObjectId to string for JSON serialization
        return jsonify(cart)
    else:
        return jsonify({'error': 'Cart not found'}), 404

    

#-------Get All User's Cart-------
@app.route('/cart', methods=['GET'])
def get_all_carts():
    carts = list(cart_collection.find({}, {'_id': 0}))
    return jsonify(carts)

@app.route('/cart/<user_id>/products', methods=['GET'])
def get_products_in_cart(user_id):
    cart = cart_collection.find_one({'user_id': user_id})
    if not cart:
        return jsonify({"error": "Cart not found"}), 404

    products_in_cart = []
    for item in cart['items']:
        product = product_collection.find_one({'_id': ObjectId(item['product_id'])})
        if product:
            product['_id'] = str(product['_id'])  # Convert ObjectId to string for JSON serialization
            products_in_cart.append(product)

    return jsonify(products_in_cart)


if __name__ == '__main__':
    app.run(debug=True)
