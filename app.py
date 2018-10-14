from flask import Flask
from flask_restplus import Api, Resource, fields


app = Flask(__name__)

api = Api(app, version='1.0', title='Book Library API',
    description='Book Library API From Team 6666',
)

bk = api.namespace('book', description='Book Library operations')

book_model = api.model('Book', {
    'id': fields.Integer(readOnly=True, description='The book id'),
    'title': fields.String(required=True, description='The book title'),
    'note': fields.String(description='Note of the book'),
    'authorId': fields.String(required=True, description='The author id of the bookd'),
    'date' : fields.String(description='Date of book release')
})

books_db = []
harry_potter = {'id' : 1, 'title' : 'Harry Potter', 'note' : 'very fun', 'authorId' : '1', 'date' : '2018-10-14'}
books_db.append(harry_potter)

query_list = []
query_list.append(harry_potter)


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


if __name__ == '__main__':
    app.run(debug=True)
