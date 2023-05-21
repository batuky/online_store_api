# online_store_api
Online Store Flask API with mongodb 


online_store
create a crud api using python and mongodb, the api should support the following operations :

    register a new user
    login users
    create | update | delete category
    create | update | delete product
    add | remove from cart
    activate | deactivate users
    display products
    filter products by category
    add to cart
    get products in cart

the app has the following collections :

    users :
        id: objectId
        username: str -> unique, required
        password : str -> required
        is_active: bool -> default true
        role: enum -> admin,client

    category
        id: objectId
        name: str -> required

    products
        id: objectId
        name: str -> required
        amount_in_stock: int -> required
        price: float -> required
        in_stock: bool -> default true

    cart

notes :

    the collection defenations above are meant to give you information about required fields,they assume nothing about db structure, feel free to come up with the best structure
    cart collection should have information about: user,selected products, count and total_price (it's up to you to decide how)
    feel free to use one of the following frameworks: Django,Flask and FastAPI

restrictions :

    inactive users can't preform the following actions : login, modify cart
    out of stock products should not be displayed
    products with 0 amount should not be displayed
    only admin users are authorized to create, update, delete products
    only admin users are authorized to create, update, delete categories
    only admin users are authorized to deactivate client users

assumptions :

    we assume you will handle edge cases to make this api as secure as possible
    only necessary information are mentioned here which means you can handle things if you feel they should be handled (even if it is not mentioned directly)
    use the best programming techniques/patterns to make the code high quality, easy to maintain, low complexity, testable
    demonstrate the knowledge of test driven development
