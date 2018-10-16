from flask_restplus import Resource, fields, Namespace

loanrec = Namespace('loan_record', description='Loan record operations')


loan_record_model = loanrec.model('LoanRecord', {
   'recordNumber': fields.Integer(readOnly=True, description='The loaner record number'),
   'bookId': fields.Integer(readOnly=True, description='The loaner id'),
   'loanerId': fields.Integer(required=True, description='The name of the loaner'),
   'loanDate': fields.String(readOnly=True, description='the loan date'),
   'returnDate': fields.String(readOnly=True, description='the return date')
   })

laon_records_db = []
one_loan_record = {'recordNumber': 101, 'bookId' : 1, 'loaner_id' : 1001,\
    'loan_date' : '181013', 'returnDate' : '181113'}
all_loan_records = [{'recordNumber': 101, 'bookId' : 1, 'loaner_id' : 1001, \
    'loan_date' : '181013', 'returnDate' : '181113'},
    {'recordNumber': 102, 'bookId': 2, 'loaner_id': 1002, \
    'loan_date': '181014', 'returnDate': '181114'}]



@loanrec.route('/<int:recordId>')
class LoanRecord(Resource):
    '''A loan record trace each loaned book information'''
    @loanrec.doc(params={'recordId' : 'a loan record id'})
    @loanrec.response(200, 'success')
    @loanrec.response(404, 'loan record not found')
    @loanrec.marshal_with(loan_record_model)
    def get(self, record_id):
        '''Get the loan record'''
        return one_loan_record, 200



@loanrec.route('/create_loan_record/<int:bookId>/<int:loanerId>/<int:loanDate>/\
<int:returnDate>')
class Create_loan_record(Resource):
    '''Create a loan record by information'''
    @loanrec.doc(params={'bookId' : 'the Id of the loaned book'})
    @loanrec.doc(params={'loanerId': 'the id of the loaner'})
    @loanrec.doc(params={'loanDate': 'the loan date of the book'})
    @loanrec.doc(params={'returnDate': 'the return date of the book'})
    @loanrec.response(200, 'success')
    @loanrec.response(400, 'creation of loan record failed')
    def put(self, book_id, loaner_id, loan_date):
        '''Create a new loan record'''
        return one_loan_record, 200


# @loanrec.route('/check_book_availability/<int:bookId>/<int:loanDate>/<int:returnDate>')
# class check_book_availability(Resource):
#     '''Check book availability'''
#     @loanrec.doc(params={'bookId': 'the Id of the loaned book'})
#     @loanrec.doc(params={'loanDate': 'the loan date of the book'})
#     @loanrec.doc(params={'returnDate': 'the return date of the book'})
#     @loanrec.response(200, 'success')
#     @loanrec.response(400, 'checking book availability failed')
#     def get(self, book_id, loan_date, return_date):
#         return one_loan_record, 200

@loanrec.route('/remind_loaner/<int:recordId>')
class Remind_loaner(Resource):
    '''Remind loaner of return'''
    @loanrec.doc(params={'recordId' : 'the Id of the loan record'})
    @loanrec.response(200, 'success')
    @loanrec.response(400, 'reminding loaner failed')
    def post(self, record_id):
        '''Send a message to loaner about returning book'''
        return one_loan_record, 200




@loanrec.route('/get_all_loan_records')
class Get_all_loan_records(Resource):
    '''Get all loan records in the database'''
    @loanrec.response(200, 'success')
    @loanrec.response(404, 'no loan record found')
    def get(self):
        '''Get all the loan records'''
        return all_loan_records, 200
