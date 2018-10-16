from flask import Flask
from flask_restplus import Api, Resource, fields


app = Flask(__name__)

api = Api(app, version='1.0', title='Book Library API',
    description='Book Library API From Team 6666',
)

bk = api.namespace('book', description='Book Library operations')
bklst = api.namespace('booklist', description='Booklist operations')
loanrec = api.namespace('loan_record', description='Loan record operations')

book_model = api.model('Book', {
    'id': fields.Integer(readOnly=True, description='The book id'),
    'title': fields.String(required=True, description='The book title'),
    'note': fields.String(description='Note of the book'),
    'authorId': fields.Integer(required=True, description='The author id of the bookd'),
    'date' : fields.String(description='Date of book release'),
    'genre': fields.String(description='Genre of the book')
})

loan_record_model = api.model('LoanRecord', {
                       'recordNumber': fields.Integer(readOnly=True, description='The loaner record number'),
                       'bookId': fields.Integer(readOnly=True, description='The loaner id'),
                       'loanerId': fields.Integer(required=True, description='The name of the loaner'),
                       'loanDate': fields.String(readOnly=True, description='the loan date'),
                       'returnDate': fields.String(readOnly=True, description='the return date')
                       })

booklist_model = api.model('Booklist', {
                       'id': fields.Integer(readOnly=True, description='The booklist id'),
                       'name': fields.String(required=True, description='The booklist name'),
                       'note': fields.String(description='Description of the booklist')
                       })


books_db = []
harry_potter = {'id' : 1, 'title' : 'Harry Potter', 'note' : 'very fun',\
'authorId' : '1', 'date' : '2018-10-14', 'genre' : 'fantasy'}
books_db.append(harry_potter)

query_list = []
query_list.append(harry_potter)

booklists_db = []
first_booklist = {'bookId' : 1, 'name' : 'First Booklist', 'note' : 'first booklist'}
booklists_db.append(first_booklist)

laon_records_db = []
one_loan_record = {'recordNumber': 101, 'bookId' : 1, 'loaner_id' : 1001,\
 'loan_date' : '181013', 'returnDate' : '181113'}
all_loan_records = [{'recordNumber': 101, 'bookId' : 1, 'loaner_id' : 1001, \
'loan_date' : '181013', 'returnDate' : '181113'},
                    {'recordNumber': 102, 'bookId': 2, 'loaner_id': 1002, \
                    'loan_date': '181014', 'returnDate': '181114'}]
booklists_db.append(first_booklist)

@bk.route('/add-book/<string:title>')
class Add_by_title(Resource):

    @bk.doc(params={'title' : 'a book title'})
    @bk.response(201, 'Book successful added')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(403, 'Can not add the book')
    def put(self, title):
        '''Add a book by book title'''
        return harry_potter, 201


@bk.route('/remove-book/<int:bookId>')
class Remove_by_id(Resource):

    @bk.doc(params={'id' : 'a book id'})
    @bk.response(200, 'Book successfully removed')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(404, 'Book not found')
    def delete(self, id):
        '''Remove a book by book id'''
        return {'message' : 'book {} has been removed.'}.format(id), 200


@bk.route('/update-book/<int:bookId>/update?authorId=<string:authorId> \
&title=<string:title>&note=<string:note>&date=<string:date>')
class Update_by_id(Resource):

    @bk.doc(params={'id' : 'a book id', 'authorId' : 'book author id', 'title' \
    : 'book title', 'note' : 'book note', 'date' : 'book release date'})
    @bk.response(200, 'Book successfully updated')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(404, 'Book not found')
    def post(self, id, author_id, title, note, date):
        '''Update a book by book id'''
        return {'message' : 'book {} has been updated.'}.format(id), 200



@bk.route('/update-book-note/<int:bookId>')
class Book_note(Resource):
    '''the note of a given book'''
    @bk.doc(params={'id' : 'a book id'})
    @bk.response(200, 'Success')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(404, 'No book found')
    def get(self, id):
        '''Get the note of a book'''
        return {'message' : 'book note found'}, 200

    @bk.doc(params={'id' : 'a book id', 'note' : 'note for a book'})
    @bk.response(200, 'Success')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(404, 'No book found')
    def put(self, id, note):
        '''Update a book note'''
        return {'message' : 'book {} has been updated.'}.format(id), 200


    @bk.doc(params={'id' : 'a book id'})
    @bk.response(200, 'Success')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(404, 'No book found')
    def delete(self, id, note):
        '''Delete the note for a book'''
        return {'message' : 'the note of book {} has been deleted.'}.format(id), 200


@bk.route('/search-by-author/search?authorId=<int:authorId>')
class Search_by_author_id(Resource):

    @bk.doc(params={'authorId' : 'Author ID'})
    @bk.response(200, 'Success')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(404, 'No author found with the given author id')
    @api.marshal_with(book_model, as_list=True)
    def get(self, author_id):
        '''Get books by author id'''
        return query_list, 200


@bk.route('/search-by-date-range/search?startDate=<string:startDate>&endDate=<string:endDate>')
class Search_by_date_range(Resource):

    @bk.doc(params={'startDate' : 'Start date of the search range', "endDate" \
    : "End date of the search range"})
    @bk.response(200, 'Success')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(404, 'No books found within the given date interval')
    @api.marshal_with(book_model, as_list=True)
    def get(self, start_date, end_date):
        '''Get books by start date and end date'''
        return query_list, 200

    # @bk.doc(params={'title' : 'the book object'},
    # response={201, 'create success', 400, 'Error'})
    # @bk.marshal_with(book_model)
    # def put(self):
    #     ''' add book into the Library'''
    #     new_book = {'id' : 5, 'title' : title, 'note' : 'very fun'}
    #     books_db.append(new_book)
    #     return {'message' : 'new book added'}, 201


@bk.route('/search_by_title/search?title=<string:title>')
class Search_by_title(Resource):

    @bk.doc(params={'title' : 'a book title'})
    @bk.response(200, 'Success')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(404, 'Book not found')
    @api.marshal_with(book_model, as_list=True)
    def get(self, title):
        '''Search a book by book title'''
        return harry_potter, 200


@bk.route('/search_by_genre/search?genre=<string:genre>')
class Search_by_genre(Resource):

    @bk.doc(params={'genre' : 'a book genre'})
    @bk.response(200, 'Success')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(404, 'Genre not found')
    def get(self, genre):
        '''Get books on a certain genre'''
        return query_list, 200


@bk.route('/advanced_search/<string:search_options>')
class Advanced_search(Resource):

    @bk.doc(params={'search_options' : 'multiple search options'})
    @bk.response(200, 'Success')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(404, 'Book not found')
    def get(self, search_options):
        '''Search books by given options'''
        return harry_potter, 200


@bklst.route('/', endpoint='/')
class Booklist(Resource):
    '''Get a booklist by booklist id'''
    @bklst.doc(params={'id' : 'a booklist id'})
    @bklst.response(200, 'Success')
    @bklst.response(400, 'Bad request, invalid syntax')
    @bklst.response(404, 'Booklist not found')
    def get(self, id):
        '''Get the booklist by the booklist id'''
        return first_booklist, 200

    @bklst.doc(params={'name' : 'the booklist name', 'note' : 'the note of \
    the booklist'})
    @bklst.response(200, 'Success')
    @bklst.response(400, 'Bad request, invalid syntax')
    @bklst.response(404, 'Booklist not found')
    @bklst.marshal_with(booklist_model)
    def put(self, name, note):
        ''' Add a booklist'''
        new_booklist = {'id' : 2, 'name' : name, 'note' : 'second booklist'}
        booklists_db.append(new_booklist)
        return {'message' : 'New booklist {} added.'}.format(name), 201

    @bklst.doc(params={'id' : 'the booklist id', 'name' : 'the booklist name', \
    'note' : 'the note of the booklist'})
    @bklst.response(200, 'Success')
    @bklst.response(400, 'Bad request, invalid syntax')
    @bklst.response(404, 'Booklist not found')
    @bklst.marshal_with(booklist_model)
    def post(self, id, name, note):
        ''' Update a booklist'''
        return {'message' : 'booklist updated'}, 201


# @bklst.route('/create_booklist/<string:list_name>')
# class create_booklist(Resource):
#     '''Create a booklist by given name'''
#     @bklst.doc(params={'list_name' : 'a booklist name'})
#     @bklst.response(201, 'booklist created success')
#     @bklst.response(400, 'booklist create error')
#     @bklst.marshal_with(booklist_model)
#     def put(self):
#         ''' add a new booklist'''
#         new_booklist = {'id' : 1, 'name' : list_name, 'note' : 'first booklist'}
#         booklists_db.append(new_booklist)
#         return {'message' : 'new booklist created'}, 201


@bklst.route('/add_book_to_a_booklist/<int:listId>/<int:bookId>')
class Add_book_to_a_booklist(Resource):
    '''group a given book into a booklist'''
    @bklst.doc(params={'listId': 'the id of the booklist'})
    @bklst.doc(params={'bookId' : 'the id of the book to be added'})
    @bklst.response(200, 'Success')
    @bklst.response(400, 'Bad request, invalid syntax')
    @bklst.response(404, 'Target book or book list not founded')
    def post(self, list_id, book_id):
        '''Add book to a certain booklist'''
        return {'message' : 'book {} has been add to booklist {}'}.\
        format(book_id, list_id), 200

@bklst.route('/remove_book_to_a_booklist/<int:listId>/<int:bookId>')
class Remove_book_to_a_booklist(Resource):
    '''Remove a given book into a booklist'''
    @bklst.doc(params={'listId': 'the id of the booklist'})
    @bklst.doc(params={'bookId' : 'the id of the book to be removed'})
    @bklst.response(200, 'Success')
    @bklst.response(400, 'Bad request, invalid syntax')
    @bklst.response(404, 'Target book or book list not founded')
    def delete(self, list_id, book_id):
        '''Remove book from a certain booklist'''
        return {'message' : 'book {} has been removed to booklist {}'}.\
        format(book_id, list_id), 200



@loanrec.route('/')
class LoanRecord(Resource):
    '''A loan record trace each loaned book information'''
    @loanrec.doc(params={'record_id' : 'a loan record id'})
    @loanrec.response(200, 'success')
    @loanrec.response(404, 'loan record not found')
    @loanrec.marshal_with(loan_record_model)
    def get(self, record_id):
        '''Get the loan record'''
        return one_loan_record, 200



@loanrec.route('/create_loan_record/<int:bookId>/<int:loanerId>/<int:loanDate>')
class Create_loan_record(Resource):
    '''Create a loan record by information'''
    @loanrec.doc(params={'recordNumber' : 'the record number'})
    @loanrec.doc(params={'bookId' : 'the Id of the loaned book'})
    @loanrec.doc(params={'loanerId': 'the id of the loaner'})
    @loanrec.doc(params={'loanDate': 'the loan date of the book'})
    @loanrec.doc(params={'returnDate': 'the return date of the book'})
    @loanrec.response(200, 'success')
    @loanrec.response(400, 'creation of loan record failed')
    def put(self, book_id, loaner_id, loan_date):
        '''create a new loan record'''
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
    @loanrec.doc(params={'record_id' : 'the Id of the loan record'})
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


if __name__ == '__main__':
    app.run(debug=True)
