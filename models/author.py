from db import db

from .exceptions import AuthorNotFoundException

class AuthorModel(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    books = db.relationship('BookModel', lazy='dynamic')

    def __init__(self, name):

        self.name = name

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'books': [book.json() for book in self.books.all()]
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def search_and_add_author(cls, name):
        cur_author = AuthorModel.find_by_name(name)
        if not cur_author:
            cur_author = AuthorModel(name)
            cur_author.save_to_db()
        return cur_author

    @classmethod
    def get_all_books_from_author(cls, author_id):
        author =  cls.query.filter_by(id=author_id).one()
        if not author:
            raise AuthorNotFoundException("no author match this id.")
        return author.books


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
