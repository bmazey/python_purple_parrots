import uuid
from flask import Flask, request, jsonify
from flask_restplus import Resource, Api
from flask_restplus import fields
from flask_sqlalchemy import SQLAlchemy

# simple flask application definition stupid
application = Flask(__name__)
api = Api(application)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(application)


message = api.model('message', {
    # 'name': fields.String(required=True, description='message title'),
    'content': fields.String(required=True, description='message content'),
})


message_id = api.model('message_id', {
    'id': fields.String(readOnly=True, description='unique identifier of a message'),
    # 'name': fields.String(required=True, description='message name'),
    'content': fields.String(required=True, description='message content'),
})


def num(bool):
    i = 0
    if bool:
        num.counter += 1
    if not bool:
        i += 1
    return num.counter


num.counter = 1


list = []


class Message(db.Model):
    id = db.Column(db.Text(80), primary_key=True)
    content = db.Column(db.String(120), unique=True, nullable=False)
    # name = db.Column(db.String(80), unique=False, nullable=False)


def __repr__(self):
    return '<Message %r>' % self.content


def create_message(data):
    id = str(uuid.uuid4())
    # static variable, not a uuid
    # id = str(num.counter)
    # {num(true): 'message'}
    # name = data.get('name')
    content = data.get('content')
    message = Message(id=id, content=content)
    # dict1 = {num(True): content}
    # list.append(dict1)
    db.session.add(message)
    db.session.commit()
    list.append(content)
    return message


@api.route("/message")
class MessageBoard(Resource):
    @api.expect(message)
    def get(self):      # @api.route("/<int:id>")
        return message

# this works, don't change post method
    @api.expect(message)
    @api.marshal_with(message_id)
    def post(self):
        new_message = create_message(request.json)
        return Message.query.filter(Message.id == new_message.id).one()


# must leave <int:id>
@api.route("/message/<string:id>")
class MessageId(Resource):
    @api.marshal_with(message_id)
    def get(self, id):
        return Message.query.filter(Message.id == id).one()


def configure_db():
    db.create_all()
    db.session.commit()


def get_app():
    return application


def main():
    configure_db()
    application.debug = True
    application.run()


if __name__ == "__main__":
    main()
