from db import db

from .book import BookModel
from .exceptions import BookNotFoundException, NoteNotFoundException


# represents the book note class
class NoteModel(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))

    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    book = db.relationship('BookModel')

    def __init__(self, book_id, input):
        self.book_id = book_id
        self.content = input

    def json(self):
        return {
            'book id': self.book_id,
            'note id': self.id,
            'note content': self.content
        }

    # find a note by its ID
    @classmethod
    def find_by_id(cls, note_id):
        return cls.query.filter_by(id=note_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    # get all notes of a book
    @classmethod
    def get_all_notes_for_book(cls, book_id):
        book = BookModel.find_by_id(book_id)
        if not book:
            raise BookNotFoundException("no book match this id.")
        return book.notes

    # create a note for a book
    @classmethod
    def create_note_for_book(cls, book_id, content):
        book = BookModel.find_by_id(book_id)
        if not book:
            raise BookNotFoundException("no book match this id.")
        note = NoteModel(book_id, content)
        note.save_to_db()
        return note

    # update an existing note
    @classmethod
    def update_note(cls, note_id, content):
        note = NoteModel.find_by_id(note_id)
        if not note:
            raise NoteNotFoundException("no note match this id.")
        note.content = content
        note.save_to_db()
        return note

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
