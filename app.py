from flask import Flask
from flask_restplus import Api, Resource, fields


app = Flask(__name__)

api = Api(app, version='1.0', title='Book Library API',
    description='Book Library API From Team 6666',
)

bk = api.namespace('book', description='Book Library operations')
bklst = api.namespace('booklist', description='Booklist operations')
loanrec = api.namespace('loanrecord', description='Loan record operations')

book_model = api.model('Book', {
    'id': fields.Integer(readOnly=True, description='The book id'),
    'title': fields.String(required=True, description='The book title'),
    'note': fields.String(description='Note of the book'),
    'authorId': fields.String(required=True, description='The author id of the bookd'),
    'date' : fields.String(description='Date of book release'),
    'genre': fields.String(description='Genre of the book')
})

loan_record_model = api.model('LoanRecord', {
                       'recordNumber': fields.Integer(readOnly=True, description='The loaner record number'),
                       'bookId': fields.Integer(readOnly=True, description='The loaner id'),
                       'loanerId': fields.Integer(required=True, description='The name of the loaner'),
                       'loanDate': fields.Integer(readOnly=True, description='the loan date'),
                       'returnDate': fields.Integer(readOnly=True, description='the return date')
                       })

booklist_model = api.model('Booklist', {
                       'id': fields.Integer(readOnly=True, description='The booklist id'),
                       'name': fields.String(required=True, description='The booklist name'),
                       'note': fields.String(description='Description of the booklist')
                       })


books_db = []
harry_potter = {'id' : 1, 'title' : 'Harry Potter', 'note' : 'very fun','authorId' : '1', 'date' : '2018-10-14', 'genre' : 'fantasy'}
books_db.append(harry_potter)

query_list = []
query_list.append(harry_potter)

booklists_db = []
first_booklist = {'bookId' : 1, 'name' : 'First Booklist', 'note' : 'first booklist'}
booklists_db.append(first_booklist)

laon_records_db = []
one_loan_record = {'recordNumber': 101, 'bookId' : 1, 'loaner_id' : 1001, 'loan_date' : 181013, 'returnDate' : 181113}
booklists_db.append(first_booklist)

@bk.route('/add-book/<string:id>')
class add_by_id(Resource):
    '''add a book by book id'''
    @bk.doc(params={'id' : 'a book id'})
    @bk.response(201, 'Book successful added')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(401, 'Unauthorized')
    @bk.response(403, 'Can not add the book')
    def put(self, title):
        return harry_potter, 201


@bk.route('/remove-book/<string:id>')
class remove_by_id(Resource):
    '''remove a book by book id'''
    @bk.doc(params={'id' : 'a book id'})
    @bk.response(200, 'Book successfully removed')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(401, 'Unauthorized')
    @bk.response(403, 'Can not remove the book')
    def put(self, title):
        return harry_potter, 200



@bk.route('/update-book/<string:id>/update?authorId=<string:authorId>&date=<string:date>&title=<string:title>d&note=<string:note>')
class update_by_id(Resource):
    '''update a book by book id'''
    @bk.doc(params={'id' : 'a book id', 'authorId' : 'book author id', 'title' : 'book title', 'note' : 'book note', 'date' : 'book release date'})
    @bk.response(200, 'Book successfully updated')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(401, 'Unauthorized')
    @bk.response(403, 'Can not update the book')
    def post(self, title):
        return harry_potter, 200


@bk.route('/search-by-author/search?authorId=<string:authorId>')
class serch_by_author_id(Resource):
    '''get books by author id'''
    @bk.doc(params={'authorId' : 'Author ID'})
    @bk.response(200, 'Success')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(403, 'Can not search by the given author id')
    @api.marshal_with(book_model, as_list=True)
    def get(self, title):
        return query_list, 200


@bk.route('/search-by-date-range/search?startDate=<string:startDate>&endDate=<string:endDate>')
class search_by_date_range(Resource):
    '''get books by start date and end date'''
    @bk.doc(params={'startDate' : 'Start date of the search range', "endDate" : "End date of the search range"})
    @bk.response(200, 'Success')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(403, 'Can not search by the given author id')
    @api.marshal_with(book_model, as_list=True)
    def get(self, title):
        return query_list, 200

    @bk.doc(params={'title' : 'the book object'},
    response={201, 'create success', 400, 'Error'})
    @bk.marshal_with(book_model)
    def put(self):
        ''' add book into the Library'''
        new_book = {'id' : 5, 'title' : title, 'note' : 'very fun'}
        books_db.append(new_book)
        return {'message' : 'new book added'}, 201


@bk.route('/search_by_title/<string:title>')
class Search_by_title(Resource):
    '''Get a book by book title'''
    @bk.doc(params={'title' : 'a book title'})
    @bk.response(200, 'success')
    @bk.response(404, 'book not found')
    def get(self, title):
        return harry_potter, 200


@bk.route('/search_by_genre/<string:genre>')
class search_by_genre(Resource):
    '''Find books on a certain genre'''
    @bk.doc(params={'genre' : 'a book genre'})
    @bk.response(200, 'success')
    @bk.response(404, 'genre not found')
    def get(self, genre):
        return harry_potter, 200


@bklst.route('/booklist', endpoint='/booklist')
class Booklist(Resource):
    '''Get a booklist by booklist id'''
    @bklst.doc(params={'id' : 'a booklist id'})
    @bklst.response(200, 'success')
    @bklst.response(404, 'booklist not found')
    def get(self, id):
        '''get the booklist'''
        return first_booklist, 200
    
    @bklst.doc(params={'name' : 'the booklist name'},
            response={201, 'create success', 400, 'Error'})
    @bklst.marshal_with(booklist_model)
    def put(self):
        ''' add a booklist'''
        new_booklist = {'id' : 2, 'name' : name, 'note' : 'second booklist'}
        booklists_db.append(new_booklist)
        return {'message' : 'new booklist added'}, 201
    def post(self):
        ''' update a booklist'''
        return {'message' : 'booklist updated'}, 201


@bklst.route('/create_booklist/<string:list_name>')
class create_booklist(Resource):
    '''Create a booklist by given name'''
    @bklst.doc(params={'list_name' : 'a booklist name'})
    @bklst.response(201, 'booklist created success')
    @bklst.response(400, 'booklist create error')
    @bklst.marshal_with(booklist_model)
    def put(self):
        ''' add a new booklist'''
        new_booklist = {'id' : 1, 'name' : list_name, 'note' : 'first booklist'}
        booklists_db.append(new_booklist)
        return {'message' : 'new booklist created'}, 201


@bklst.route('/add_books_to_a_booklist/<int:listId>/<string:bookIds>')
class add_books_to_a_booklist(Resource):
    '''group given books into a booklist'''
    @bklst.doc(params={'listId': 'the id of the booklist'})
    @bklst.doc(params={'bookIds' : 'the Ids of the books to be added'})
    @bklst.response(200, 'books added to the list successfully')
    @bklst.response(400, 'books added to the list unsuccessfully')
    def post(self, listId, bookIds):
        return None, 200


@bk.route('/advanced_search/<string:search_options>')
class advanced_search(Resource):
    '''search books by given conditions'''
    @bk.doc(params={'search_options' : 'multiple constraints for searching qualified books'})
    @bk.response(200, 'success')
    @bk.response(404, 'book not found')
    def get(self, search_options):
        return harry_potter, 200





@loanrec.route('/loan_record', endpoint='/loan_record')
class LoanRecord(Resource):
    @loanrec.doc(params={'recordNumber' : 'a loan record number'})
    @loanrec.response(200, 'success')
    @loanrec.response(404, 'loan record not found')
    @loanrec.marshal_with(loan_record_model)
    def get(self, recordNumber):
        '''get the loan record'''
        return one_loan_record, 200



@loanrec.route('/create_loan_record/<int:bookId>/<int:loanerId>/<int:loanDate>')
class create_loan_record(Resource):
    '''Create a loan record by information'''
    @loanrec.doc(params={'recordNumber' : 'the record number'})
    @loanrec.doc(params={'bookId' : 'the Id of the loaned book'})
    @loanrec.doc(params={'loanerId': 'the id of the loaner'})
    @loanrec.doc(params={'loanDate': 'the loan date of the book'})
    @loanrec.doc(params={'returnDate': 'the return date of the book'})
    @loanrec.response(200, 'success')
    @loanrec.response(400, 'creation of loan record failed')
    def put(self, bookId, loanerId, loanDate):
        return one_loan_record, 200


if __name__ == '__main__':
    app.run(debug=True)
