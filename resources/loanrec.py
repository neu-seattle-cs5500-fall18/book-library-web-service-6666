from flask_restplus import Resource, Namespace
from models.loan_record import LoanRecordModel
from models.book import BookModel
from models.user import UserModel
from .book import DateRead
from utils.send_email import EmailSender

loanrec = Namespace('loan_record', description='Loan record operations')


@loanrec.route('/<int:book_id>')
class GetLoanRecordsForBook(Resource):
    '''A loan record trace each loaned book information'''
    @loanrec.doc(params={'book_id' : 'a book id'})
    @loanrec.response(200, 'success')
    @loanrec.response(404, 'loan record not found')
    def get(self, book_id):
        '''Get the loan record'''
        try:
            book = BookModel.find_by_id(book_id)
        except Exception as e:
            return {'message' : 'book {} not found'.format(book_id)}, 404
        loan_records = LoanRecordModel.find_by_book_id(book_id)
        return [loan_rec.json() for loan_rec in loan_records], 200



@loanrec.route('/loan_book/<int:book_id>/<int:user_id>/<string:loan_date>/<string:due_date>')
class LoanBook(Resource):
    '''Create a loan record by information'''
    @loanrec.doc(params={'book_id' : 'the Id of the loaned book'})
    @loanrec.doc(params={'user_id': 'the id of the loaner'})
    @loanrec.doc(params={'loan_date': 'the loan date of the book', 'due_date' : 'return due date'})
    @loanrec.response(201, 'success')
    @loanrec.response(400, 'creation of loan record failed')
    def post(self, book_id, user_id, loan_date, due_date):
        '''Create a new loan record'''
        loan_day = DateRead.read_date(loan_date)
        due_day = DateRead.read_date(due_date)
        try:
            book = BookModel.find_by_id(book_id)
        except Exception as e:
            return {'message' : 'loan book error, book or user not found'}, 400
        if not BookModel.check_availability(book):
            return {'message' : 'book {} has been loaned out'.format(book_id)}, 400
        loanrec = LoanRecordModel.create_loan_record(book_id, user_id, loan_day, due_day)
        BookModel.mark_loaned_out(book)
        return loanrec.json(), 201

@loanrec.route('/return_book/<int:rec_id>/<string:return_date>')
class ReturnBook(Resource):
    '''Return a book to complete the loan record'''
    @loanrec.doc(params={'rec_id' : 'the loan record id', 'return_date' : 'the return date of loan'})
    @loanrec.response(200, 'success')
    @loanrec.response(400, 'creation of loan record failed')
    def post(self, rec_id, return_date):
        return_day = DateRead.read_date(return_date)
        try:
            loan_rec = LoanRecordModel.find_by_id(rec_id)
            book = BookModel.find_by_id(loan_rec.book_id)
        except Exception as e:
            return {'message' : 'Error, cannot find this loan record'}, 400
        LoanRecordModel.complete_loan_record(loan_rec.id, return_day)
        BookModel.mark_returned(book)
        return {'message' : 'book {} is successfully returned'.format(book.id)}, 200


@loanrec.route('/remind_loaner/<int:loan_rec_id>')
class RemindLoaner(Resource):
    @loanrec.doc(params={'loan_rec_id' : 'the loan record'})
    @loanrec.response(200, 'success')
    @loanrec.response(404, 'no loan record found')
    def post(self, loan_rec_id):
        '''return the loaner to return book on time'''
        loan_rec = LoanRecordModel.find_by_id(loan_rec_id)
        if not loan_rec:
            return {'message' : 'no loan record match this id'}, 404
        due_date = loan_rec.due_date
        user_id = loan_rec.user_id
        user = UserModel.find_by_id(user_id)
        email_rev = user.email
        book_id = loan_rec.book_id
        book = BookModel.find_by_id(book_id)
        try:
            EmailSender.send_email(email_rev, user.name, book.name, due_date.strftime('%m/%d/%Y'))
            return {'message' : 'Reminder sent successfully.'}
        except Exception as e:
            return {'message' : 'error sending the reminder'}, 400


@loanrec.route('/get_all_loan_records')
class GetAllLoanRecords(Resource):
    '''Get all loan records in the database'''
    @loanrec.response(200, 'success')
    @loanrec.response(404, 'no loan record found')
    def get(self):
        '''Get all the loan records'''
        return [rec.json() for rec in LoanRecordModel.find_all()], 200

