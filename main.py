import requests
import json

# -------USER------- 

#-------Login an User------- 
# login_data = {
#     'username': 'admin',
#     'password': 'admin'
# }

# response = requests.post('http://localhost:5000/login', json=login_data)

# if response.status_code == 200:
#     result = response.json()
#     print('Login success.')
#     print('User role:', result['role'])
#     token = result['token']  # Retrieve the JWT token from the response
#     # Use the token for further authenticated requests
#     headers = {'Authorization': 'Bearer ' + token}
#     # Make authenticated requests with the headers containing the token
# else:
#     print('Login error:', response.json())

# -------Create an User------- 
# url = 'http://localhost:5000/users'

# data = {
#     'username': 'democlient',
#     'password': 'democlient',
#     'confirm_password': 'democlient',
#     'is_active': 'false',
#     'role': 'client'
# }

# response = requests.post(url, data=data)

# print(response.json())

# -------Get All Users------- 
# url = 'http://localhost:5000/users'

# response = requests.get(url)

# print(response.json())

# -------Get a Specific User------- 
# user_id = '4'  # Replace with the actual user ID
# url = f'http://localhost:5000/users/{user_id}'

# response = requests.get(url)

# print(response.json())

# -------Update an User------- 

# user_id = '3'  # Replace with the actual user ID
# url = f'http://localhost:5000/users/{user_id}'

# data = {
#     'username': 'demoadmin1Updated',
#     'password': 'demoadmin1',
#     'confirm_password': 'demoadmin1',
#     'is_active': 'true',
#     'role': 'admin'
# }

# response = requests.put(url, data=data)

# print(response.json())


# -------Delete an User------- 
# user_id = '5'  # Replace with the actual user ID
# url = f'http://localhost:5000/users/{user_id}'

# response = requests.delete(url)

# print(response.json())

# -------Activate an User------- 
# user_id = '2'  # Replace with the actual user ID

# response = requests.put(f'http://localhost:5000/users/{user_id}/activate')

# if response.status_code == 200:
#     try:
#         result = response.json()
#         print(result['message'])
#     except json.JSONDecodeError:
#         print('Invalid JSON response from the server')
# else:
#     try:
#         error = response.json()
#         print('Failed to activate user:', error)
#     except json.JSONDecodeError:
#         print('Invalid JSON response from the server')



# -------Deactivate an User------- 
# user_id = '2'  # Replace with the actual user ID

# headers = {
#     'User-ID': '1'  # Replace with the actual user ID
# }

# response = requests.put(f'http://localhost:5000/users/{user_id}/deactivate', headers=headers)

# if response.status_code == 200:
#     result = response.json()
#     print(result['message'])
# else:
#     error = response.json()
#     print('Failed to deactivate user:', error)


# -------CATEGORY------- 
# -------Create a Category------- 
# headers = {'User-ID': '1'}  # write user int id number

# category_data = {'name': 'Hardware'}

# response = requests.post('http://localhost:5000/categories', json=category_data, headers=headers)

# if response.status_code == 201:
#     result = response.json()
#     print('Category created successfully.')
#     print('Category ID:', result['id'])
# else:
#     print('Category creation failed:', response.json())


# -------Update a Category------- 
# headers = {'User-ID': '1'}  # Assuming the admin user ID is provided in the headers

# category_id = '646a6e4431a9757799df7ac6'  # Replace with the actual category ID
# category_data = {'name': 'Books'}  # Replace with the updated category data

# response = requests.put(f'http://localhost:5000/categories/{category_id}', json=category_data, headers=headers)

# if response.status_code == 200:
#     result = response.json()
#     print('Category updated successfully.')
# else:
#     print('Category update failed:', response.json())

# -------Delete a Category------- 
# headers = {'User-ID': '1'}  # Assuming the admin user ID is provided in the headers

# category_id = '646a6e4431a9757799df7ac6'  # Replace with the actual category ID

# response = requests.delete(f'http://localhost:5000/categories/{category_id}', headers=headers)

# if response.status_code == 200:
#     result = response.json()
#     print('Category deleted successfully.')
# else:
#     print('Category deletion failed:', response.json())


# -------PRODUCT------- 
# -------Create a Product------- 
# headers = {'User-ID': '1'}  # Assuming the admin user ID is provided in the headers

# product_data = {
#     'name': 'Screw Driver',
#     'amount_in_stock': 10,
#     'price': 19.99,
#     'in_stock': True,
#     'category_id': '646a6e9131a9757799df7ac9'  # Replace with the actual category ID
# }

# response = requests.post('http://localhost:5000/products', data=product_data, headers=headers)

# if response.status_code == 201:
#     result = response.json()
#     print('Product created successfully.')
#     print('Product ID:', result['id'])
# else:
#     print('Product creation failed:', response.json())

# -------Update a Product------- 
# headers = {'User-ID': '1'}  # Assuming the admin user ID is provided in the headers

# product_data = {
#     'name': 'Screw Driver',
#     'price': 24.99,
#     'amount_in_stock': 5
# }

# product_id = '646a736be8c641faa8ee7a23'  # Replace with the actual product ID

# response = requests.put(f'http://localhost:5000/products/{product_id}', json=product_data, headers=headers)

# if response.status_code == 200:
#     print('Product updated successfully.')
# else:
#     print('Product update failed:', response.json())

# -------Delete a Product------- 
# headers = {'User-ID': '1'}  # Assuming the admin user ID is provided in the headers

# product_id = '646a736be8c641faa8ee7a23'  # Replace with the actual product ID

# response = requests.delete(f'http://localhost:5000/products/{product_id}', headers=headers)

# if response.status_code == 200:
#     print('Product deleted successfully.')
# else:
#     print('Product deletion failed:', response.json())

# -------Get All Products------- 
# response = requests.get('http://localhost:5000/products')

# if response.status_code == 200:
#     products = response.json()
#     for product in products:
#         print('Product:', product)
# else:
#     print('Failed to retrieve products:', response.json())


# -------Get a Spesific Product------- 
# product_id = '646a732be8c641faa8ee7a20'  # Replace with the actual product ID

# response = requests.get(f'http://localhost:5000/products/{product_id}')

# if response.status_code == 200:
#     product = response.json()
#     print('Product:', product)
# else:
#     print('Failed to retrieve product:', response.json())


# -------Get Products by Category------- 
# category_id = '646a6e5c31a9757799df7ac7'  # Replace with the actual category ID

# response = requests.get(f'http://localhost:5000/products_by_category/{category_id}')

# if response.status_code == 200:
#     products = response.json()
#     print('Products:', products)
# else:
#     print('Failed to retrieve products:', response.json())


#-------CART-------
#-------Add a Product to Cart-------

# url = 'http://localhost:5000/cart/add'
# headers = {
#     'User-ID': '1',
#     'Content-Type': 'application/json'
# }
# data = {
#     'user_id': 1,
#     'product_id': '646a732be8c641faa8ee7a20',
#     'quantity': 3
# }

# response = requests.post(url, headers=headers, json=data)

# if response.status_code == 200:
#     result = response.json()
#     print(result['message'])
# else:
#     error = response.json()
#     print(f"An error occurred: {error['error']}")


#-------Delete a Product to Cart-------
# url = 'http://localhost:5000/cart/remove'
# headers = {
#     'User-ID': '1',
#     'Content-Type': 'application/json'
# }
# data = {
#     'user_id': 1,
#     'cart_id': '646a7e3e9157df2f06bac609',  # Specify the cart ID
#     'product_id': '646a72f8e8c641faa8ee7a1e'
# }

# response = requests.post(url, headers=headers, json=data)

# if response.status_code == 200:
#     result = response.json()
#     print(result['message'])
# else:
#     error = response.json()
#     print(f"An error occurred: {error['error']}")

#-------Get Products From an User's Cart-------
# Specify the URL and user ID
# user_id = '1'  # Specify the user ID for which you want to retrieve the cart

# url = f'http://localhost:5000/cart/{user_id}'
# headers = {'User-ID': user_id}

# response = requests.get(url, headers=headers)

# if response.status_code == 200:
#     cart = response.json()
#     print(cart)
# else:
#     error = response.json()
#     print(f"An error occurred: {error}")

#-------Get All Carts-------
# response = requests.get('http://localhost:5000/cart')
# carts = response.json()
# print(carts)