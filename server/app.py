#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

@app.route('/games')
def games():

    games = []
    for game in Game.query.all():
        game_dict = {
            "title": game.title,
            "genre": game.genre,
            "platform": game.platform,
            "price": game.price,
        }
        games.append(game_dict)

    response = make_response(
        games,
        200
    )

    return response

@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    
    game_dict = game.to_dict()

    response = make_response(
        game_dict,
        200
    )

    return response

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():

    if request.method == 'GET':
        reviews = []
        for review in Review.query.all():
            review_dict = review.to_dict()
            reviews.append(review_dict)

        response = make_response(
            reviews,
            200
        )
        return response
    elif request.method == 'POST':
        json_data = request.get_json()
        new_review = Review(
           score = json_data.get('score'),
           comment = json_data.get('comment'),
           game_id = json_data.get('game_id'),
           user_id = json_data.get('user_id')
        )
        db.session.add(new_review)
        db.session.commit()
        return new_review.to_dict(), 201

@app.route('/reviews/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
def review_by_id(id):
    review = Review.query.filter_by(id=id).first()
    if not review:
        return {"error": f"Review with id {id} does not exist"}, 404

    if request.method == 'GET':
        return review.to_dict(), 200
    elif request.method == 'DELETE':
        x = review.to_dict()
        db.session.delete(review)
        db.session.commit()
        return x, 200
    elif request.method == 'PATCH':
        json_data = request.get_json()
        for key, value in json_data.items():
            setattr(review, key, value)
        db.session.add(review)
        db.session.commit()
        return review.to_dict(), 200

@app.route('/users')
def users():

    users = []
    for user in User.query.all():
        user_dict = user.to_dict()
        users.append(user_dict)

    response = make_response(
        users,
        200
    )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
