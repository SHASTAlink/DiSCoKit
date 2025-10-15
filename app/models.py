"""
Database models for experimental chat application.
"""

from datetime import datetime
from app import db


class Participant(db.Model):
    """Store participant information and experimental condition assignment."""
    __tablename__ = 'participants'
    
    participant_id = db.Column(db.String(255), primary_key=True)
    session_token = db.Column(db.String(64), nullable=False, unique=True, index=True)
    condition_index = db.Column(db.Integer, nullable=False)
    condition_id = db.Column(db.String(100), nullable=False)
    condition_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to messages
    messages = db.relationship('Message', backref='participant', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'participant_id': self.participant_id,
            'condition_index': self.condition_index,
            'condition_id': self.condition_id,
            'condition_name': self.condition_name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
            # Note: session_token intentionally excluded from export for security
        }


class Message(db.Model):
    """Store individual messages in conversations."""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.String(255), db.ForeignKey('participants.participant_id'), nullable=False, index=True)
    role = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Composite index for the most common query pattern (filter by participant_id, order by timestamp)
    __table_args__ = (
        db.Index('ix_messages_participant_timestamp', 'participant_id', 'timestamp'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'participant_id': self.participant_id,
            'role': self.role,
            'content': self.content,
            'timestamp': self.timestamp.isoformat()
        }