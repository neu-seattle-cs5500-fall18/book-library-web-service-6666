from db import db

from .exceptions import BookNotFoundException


class BookModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    author = db.relationship('AuthorModel')

    release_date = db.Column(db.Date)

    genre_id = db.Column(db.String(80), db.ForeignKey('genres.id'))
    genre = db.relationship('GenreModel')

    is_loaned_out = db.Column(db.Boolean, default=False)

    notes = db.relationship('NoteModel', lazy='dynamic')


    def __init__(self, name, author_id, date, genre):
        self.name = name
        self.author_id = author_id
        self.release_date = date
        self.genre = genre

    def json(self):
        return {
            'id': self.id,
            'title': self.name,
            'author id': self.author_id,
            'release date': self.release_date.strftime('%m/%d/%Y'),
            'genre': self.genre.name,
            'is loaned out': self.is_loaned_out
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def update_book(cls, book_id, name, author, date, genre):
        book = BookModel.find_by_id(book_id)
        if not book:
            raise BookNotFoundException("no book match this id")
        book.name = name
        book.author_id = author.id
        book.author = author
        book.release_date = date
        book.genre = genre
        book.genre_id = genre.id
        book.save_to_db()
        return book

    @classmethod
    def find_by_date_range(cls, start_date, end_date):

        return cls.query.filter(cls.release_date >= start_date, cls.release_date <= end_date).all()




    def mark_loaned_out(self):
        self.is_loaned_out = True
        self.save_to_db()

    def mark_returned(self):
        self.is_loaned_out = False
        self.save_to_db()

    def check_availability(self):
        return not self.is_loaned_out



    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()