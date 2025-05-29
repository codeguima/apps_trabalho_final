from .extensions import db

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    user_id_send = db.Column(db.Integer, nullable=False)
    user_id_received = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'user_id_send': self.user_id_send,
            'user_id_received': self.user_id_received,
        }
