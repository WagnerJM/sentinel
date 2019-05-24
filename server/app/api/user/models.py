import bcrypt

from app.database import BaseMixin, db
from app.serializer import ma


class User(db.Model, BaseMixin):
    __tablename__ = 'user_table'

    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    _password = db.Column(db.Binary(60))
    email = db.Column(db.String, nullable=False)
    
    guest = db.Column(db.Boolean, default=False)
    user = db.Column(db.Boolean, default=True)
    admin = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, email):
        self.username = username
        self._password = self.hash_pw(password).encode('utf-8')
        self.email = email

    def check_pw(self, hashed_pw, password):
        return bcrypt.checkpw(password.encode('utf-8'), hash_pw)

    
    def hash_pw(self, password):
        return bcrypt.hashpw(password, bcrypt.gensalt(12))

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        fields = (
                "id",
                "username",
                "email",
                "guest",
                "user",
                "admin"
                )
    
        

    
