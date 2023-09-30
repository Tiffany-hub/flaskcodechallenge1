# Pizza Restaurant API

This is a simple Flask-based API for managing pizza restaurants and their menus. It provides endpoints for creating, retrieving, and deleting restaurants, as well as managing pizzas associated with each restaurant.

## Setup

1. Clone the repository.
2. Install the required packages using `pip install -r requirements.txt`.
3. Run the application with `python app.py`.

## Endpoints

### Get All Restaurants

- **URL**: `/restaurants`
- **Method**: `GET`
- **Response**: List of all restaurants with their IDs, names, and addresses.

### Get Restaurant by ID

- **URL**: `/restaurants/<int:id>`
- **Method**: `GET`
- **Parameters**:
  - `id`: ID of the restaurant.
- **Response**: Details of the restaurant with the specified ID, including its name, address, and list of pizzas.

### Delete Restaurant

- **URL**: `/restaurants/<int:id>`
- **Method**: `DELETE`
- **Parameters**:
  - `id`: ID of the restaurant to be deleted.
- **Response**: No content (HTTP status code 204) if successful. If the restaurant is not found, an error message is returned with a 404 status code.

### Get All Pizzas

- **URL**: `/pizzas`
- **Method**: `GET`
- **Response**: List of all pizzas with their IDs, names, and ingredients.

### Create Restaurant Pizza

- **URL**: `/restaurant_pizzas`
- **Method**: `POST`
- **Request Body**:
  - `price`: Price of the pizza.
  - `pizza_id`: ID of the pizza.
  - `restaurant_id`: ID of the restaurant.
- **Response**: Details of the created pizza, including its ID, name, and ingredients. If there are validation errors (e.g., duplicate entry), an error message is returned with a 400 status code.

## Models

### Restaurant

- **Fields**:
  - `id` (Integer, Primary Key): Unique identifier for the restaurant.
  - `name` (String, 50 characters, Unique, Not Null): Name of the restaurant.
  - `address` (String, 255 characters, Not Null): Address of the restaurant.

### Pizza

- **Fields**:
  - `id` (Integer, Primary Key): Unique identifier for the pizza.
  - `name` (String, 50 characters, Not Null): Name of the pizza.
  - `ingredients` (String, 255 characters, Not Null): Ingredients used in the pizza.

### RestaurantPizza

- **Fields**:
  - `id` (Integer, Primary Key): Unique identifier for the association.
  - `price` (Float, Not Null): Price of the pizza in the restaurant.
  - `restaurant_id` (Integer, Foreign Key to Restaurant, Not Null): ID of the associated restaurant.
  - `pizza_id` (Integer, Foreign Key to Pizza, Not Null): ID of the associated pizza.

## Database

The application uses a SQLite database (`pizzarestaurants.db`) to store restaurant, pizza, and association information.

## Running the Application

1. Ensure you have Python and Flask installed.
2. Set up the database by running the application.
3. Use API endpoints to manage restaurants and pizzas.
