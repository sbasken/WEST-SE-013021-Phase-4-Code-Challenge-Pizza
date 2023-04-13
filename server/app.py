#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

class Restaurants(Resource):

    def get(self):
        restaurants_dict = [ r.to_dict() for r in Restaurant.query.all() ]
        return restaurants_dict

api.add_resource(Restaurants, '/restaurants')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
