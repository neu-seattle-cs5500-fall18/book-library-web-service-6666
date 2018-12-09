from db import db
from .exceptions import AuthorNotFoundException

# book_list_table = db.Table('book_lists',
#                            db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True),
#                            db.Column('book_list_id', db.Integer, db.ForeignKey('BookLists.id'), primary_key=True))


class ListBookAssociation(db.Model):
    __tablename__ = 'list_book_table'
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('BookLists.id'), primary_key=True)

    book = db.relationship("BookModel")
    list = db.relationship('BookListModel', backref=db.backref("book",
                                                               cascade="save-update, merge, delete, delete-orphan"))

    def __init__(self, list_id, book_id):

        self.list_id = list_id
        self.book_id = book_id


    def json(self):
        return {
            'book id' : self.book_id,
            'list id' : self.list_id
        }

    @classmethod
    def find_by_id(cls, list_id, book_id):
        return cls.query.filter_by(list_id=list_id, book_id=book_id).first()

    @classmethod
    def create_an_association(cls, list_id, book_id):
        book_list_asso = ListBookAssociation.find_by_id(list_id, book_id)
        if not book_list_asso:
            book_list_asso = ListBookAssociation(list_id, book_id)
            book_list_asso.save_to_db()
        return book_list_asso


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()




class BookListModel(db.Model):
    __tablename__ = 'BookLists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    books = db.relationship('ListBookAssociation')

    def __init__(self, name):

        self.name = name

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'books': [book_assoc.book_id for book_assoc in self.books]
        }

    def add_new_book(self, book_id):
        # self.book_ids.remove(book_id)
        db.session.add(book_id)
        db.session.commit()

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
    def create_a_list(cls, name):
        book_list = BookListModel.find_by_name(name)
        if not book_list:
            book_list = BookListModel(name)
            book_list.save_to_db()
        return book_list

    @classmethod
    def get_all_books_from_list(cls, book_list_id):
        book_list = cls.query.filter_by(id=book_list_id).one()
        if not book_list:
            raise AuthorNotFoundException("no author match this id.")
        return book_list.books


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
