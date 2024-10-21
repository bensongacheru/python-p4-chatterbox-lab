from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# GET /messages: Get all messages
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages])

# POST /messages: Create a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    if not data or not data.get('body') or not data.get('username'):
        return jsonify({'error': 'Invalid input'}), 400

    new_message = Message(
        body=data['body'],
        username=data['username'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201

# PATCH /messages/<int:id>: Update a message by ID
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = db.session.get(Message, id)  # Updated line
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    
    data = request.get_json()
    if 'body' in data:
        message.body = data['body']
    db.session.commit()
    
    return jsonify(message.to_dict()), 200

# DELETE /messages/<int:id>: Delete a message by ID
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.get(Message, id)  # Updated line
    if message:
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'Message deleted successfully'}), 200
    else:
        return jsonify({'error': 'Message not found'}), 404

if __name__ == '__main__':
    app.run(port=5555)
