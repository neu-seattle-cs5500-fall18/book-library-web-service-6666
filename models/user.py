from db import db


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

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def create_new_user(cls, name, email):
        new_user = UserModel(name, email)
        new_user.save_to_db()
        return new_user

    # @classmethod
    # def search_and_add_genre(cls, name):
    #     cur_genre = GenreModel.find_by_name(name)
    #     if not cur_genre:
    #         cur_genre = GenreModel(name)
    #         cur_genre.save_to_db()
    #     return cur_genre
    #
    # @classmethod
    # def get_all_books_from_genre(cls, name):
    #     genre =  cls.query.filter_by(name=name).one()
    #     if not genre:
    #         raise Exception("no author match this id.")
    #     return genre.books


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
