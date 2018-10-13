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
    'note': fields.String(description='Note of the book')
})

books_db = []
harry_potter = {'id' : 1, 'title' : 'Harry Potter', 'note' : 'very fun'}
books_db.append(harry_potter)



@bk.route('/book', endpoint='/book')
class Book(Resource):
    '''Get a book by book id'''
    @bk.doc(params={'id' : 'a book id'})
    @bk.response(200, 'success')
    @bk.response(404, 'book not found')
    def get(self, id):
        '''get the book'''
        return harry_potter, 200

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

if __name__ == '__main__':
    app.run(debug=True)
