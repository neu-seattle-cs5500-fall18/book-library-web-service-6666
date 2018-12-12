from db import db


# represents the user class
class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)

    book_records = db.relationship('LoanRecordModel', lazy='dynamic')

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'loan records': [loan_rec.json() for loan_rec in self.book_records.all()]
        }

    # find a user by name
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    # find a user by ID
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    # create a new user
    @classmethod
    def create_new_user(cls, name, email):
        new_user = UserModel(name, email)
        new_user.save_to_db()
        return new_user

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
