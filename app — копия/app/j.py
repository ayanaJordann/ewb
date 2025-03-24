from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify, make_response
import db_session
from . users import User


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('about', required=True)
parser.add_argument('email', required=True)
parser.add_argument('hashed_password', required=True)
parser.add_argument('created_date', required=True)

def abort_if_news_not_found(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        abort(404, message=f"News {user_id} not found")

class NewsResource(Resource):
    def get(self, news_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        users = session.query(User).get(news_id)
        return jsonify({'users': users.to_dict()})

    def delete(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        news = session.query(User).get(user_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})

class NewsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(User).all()
        return jsonify({'users': [item.to_dict() for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        news = User(
            title=args['title'],
            content=args['content'],
            user_id=args['user_id'],
            is_published=args['is_published'],
            is_private=args['is_private']
        )
        session.add(news)
        session.commit()
        return jsonify({'id': news.id})