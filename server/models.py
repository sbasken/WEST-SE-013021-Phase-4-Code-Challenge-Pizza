from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here

class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    restraunt_pizzas = db.relationship("RestaurantPizza", back_populates="pizza")
    restaurants = association_proxy('restraunt_pizzas', 'restaurant')

    serialize_rules = ( '-created_at', '-updated_at', '-restaurant_pizzas', 'restaurants')

    def __repr__(self):
        return f"<Pizza Name: {self.name}, Ingredients: {self.ingredients}>"
    
class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))

    pizza = db.relationship("Pizza", backref="restaurant_pizzas")
    restaurant = db.relationship("Restaurant", backref="restaurant_pizzas")

    serialize_rules = ( '-created_at', '-updated_at')

    def __repr__(self):
        return f"<RestaurantPizza Price: {self.price}, Pizza: {self.pizza_id}, Restaurant: {self.restaurant_id}>"

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    restraunt_pizzas = db.relationship("RestaurantPizza", back_populates="restaurant")
    pizzas = association_proxy('restraunt_pizzas', 'pizza')

    serialize_rules = ( 'restaurant_pizzas', 'pizzas')

    def __repr__(self):
        return f"<Restaurant Name: {self.name}, Address: {self.address}>"
                         