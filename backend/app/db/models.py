from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField
from datetime import datetime

class User(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    password_hash = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)

class Resume(Document):
    user = ReferenceField(User, required=True)
    title = StringField(required=True)
    content = StringField(required=True)
    uploaded_at = DateTimeField(default=datetime.utcnow)
    tags = ListField(StringField())