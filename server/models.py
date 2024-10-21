from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)  # Message content
    username = db.Column(db.String, nullable=False)  # Username of the person sending the message
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of message creation
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp of last update

    # This method serializes the model into a dictionary for JSON responses
    def to_dict(self):
        return {
            'id': self.id,
            'body': self.body,
            'username': self.username,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
