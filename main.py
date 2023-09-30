from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizzarestaurants.db'
db = SQLAlchemy(app)

# Define models
class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pizzas = db.relationship('Pizza', secondary='restaurant_pizza', backref=db.backref('restaurants', lazy='dynamic'))

class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)

class RestaurantPizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Define routes
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([{'id': r.id, 'name': r.name, 'address': r.address} for r in restaurants])

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        return jsonify({
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'pizzas': [{'id': p.id, 'name': p.name, 'ingredients': p.ingredients} for p in restaurant.pizzas]
        })
    return jsonify({'error': 'Restaurant not found'}), 404

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    return jsonify({'error': 'Restaurant not found'}), 404

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'ingredients': p.ingredients} for p in pizzas])

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    try:
        restaurant_pizza = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
        db.session.add(restaurant_pizza)
        db.session.commit()
        return jsonify({'id': pizza_id, 'name': Pizza.query.get(pizza_id).name, 'ingredients': Pizza.query.get(pizza_id).ingredients}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'errors': ['validation errors']}), 400

if __name__ == '__main__':
    app.run(debug=True)
