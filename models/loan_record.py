from db import db

from models.book import BookModel
from models.user import UserModel

from .exceptions import BookNotFoundException, UserNotFoundException, RecordNotFoundException

class LoanRecordModel(db.Model):
    __tablename__ = 'loan_record_table'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    loan_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    returned_on_time = db.Column(db.Boolean, default=False)

    book = db.relationship("BookModel", backref=db.backref("book",
                                                               cascade="save-update, merge, delete, delete-orphan"))
    loaner = db.relationship('UserModel', backref=db.backref("user",
                                                               cascade="save-update, merge, delete, delete-orphan"))

    def __init__(self, book_id, user_id, loan_date, due_date):

        self.book_id = book_id
        self.user_id = user_id
        self.loan_date = loan_date
        self.due_date = due_date

    def json(self):
        return {
            'loan record id' : self.id,
            'book id' : self.book_id,
            'user id' : self.user_id,
            'loan date' : self.loan_date.strftime('%m/%d/%Y'),
            'due date' : self.due_date.strftime('%m/%d/%Y'),
            'returned on time' : self.returned_on_time
        }

    @classmethod
    def find_by_id(cls, rec_id):
        return cls.query.filter_by(id=rec_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_book_id(cls, book_id):
        return cls.query.filter_by(book_id=book_id)




    @classmethod
    def create_loan_record(cls, book_id, user_id, loan_date, due_date):
        book = BookModel.find_by_id(book_id)
        if not book:
            raise BookNotFoundException("no book match this id")
        user = UserModel.find_by_id(user_id)
        if not user:
            raise UserNotFoundException("no user match this id")
        new_record = LoanRecordModel(book_id, user_id, loan_date, due_date)
        new_record.save_to_db()
        return new_record

    @classmethod
    def complete_loan_record(cls, rec_id, return_day):
        record = LoanRecordModel.find_by_id(rec_id)
        if not record:
            raise RecordNotFoundException("no record match this id")
        record.return_date = return_day
        record.returned_on_time = return_day < cls.due_date
        record.save_to_db()
        return record


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
