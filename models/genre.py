from db import db

from .exceptions import GenreNotFoundException


# represents the book genre class
class GenreModel(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    books = db.relationship('BookModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'books': [book.json() for book in self.books.all()]
        }

    # find a genre by its name
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    # search for a given genre and return it. If not exist, create the genre and return it
    @classmethod
    def search_and_add_genre(cls, name):
        cur_genre = GenreModel.find_by_name(name)
        if not cur_genre:
            cur_genre = GenreModel(name)
            cur_genre.save_to_db()
        return cur_genre

    # get all the books of a given genre
    @classmethod
    def get_all_books_from_genre(cls, name):
        genre = cls.query.filter_by(name=name).one()
        if not genre:
            raise GenreNotFoundException("no genre match this id.")
        return genre.books

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
