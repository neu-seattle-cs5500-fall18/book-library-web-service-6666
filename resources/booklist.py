from flask_restplus import Resource, fields, Namespace
from models.booklist import BookListModel, ListBookAssociation
from models.book import BookModel


bklst = Namespace('booklist', description='booklist operations')



@bklst.route('/<string:name>')
class CreateBookList(Resource):
    @bklst.doc(params={'name': 'the book list name'})
    @bklst.response(201, 'Success')
    @bklst.response(400, 'Bad request, invalid syntax')

    def post(self, name):
        ''' Add a booklist'''
        new_book_list = BookListModel.create_a_list(name)
        return new_book_list.json(), 201

@bklst.route('/<int:list_id>')
class GetBookList(Resource):
    @bklst.doc(params={'list_id': 'the book list id'})
    @bklst.response(200, 'Success')
    @bklst.response(400, 'Bad request, invalid syntax')
    def get(self, list_id):
        ''' Get a book list'''
        book_list = BookListModel.find_by_id(list_id)
        if not book_list:
            return {'message': 'book list {} not found'.format(list_id)}, 404
        return book_list.json(), 200

@bklst.route('/remove_whole_list/<int:list_id>')
class RemoveBookList(Resource):
    @bklst.doc(params={'list_id': 'the book list id'})
    @bklst.response(200, 'Success')
    @bklst.response(400, 'Bad request, invalid syntax')
    def delete(self, list_id):
        ''' Remove a book list'''
        book_list = BookListModel.find_by_id(list_id)
        if not book_list:
            return {'message' : 'book list {} not found'.format(list_id)}, 404
        book_list.delete_from_db()
        return {'message' : 'book list {} has been removed'.format(list_id)}, 200



@bklst.route('/add_book_to_a_book_list/<int:list_id>/<int:book_id>')
class AddBookToABookList(Resource):
    '''Group a given book into a book list'''
    @bklst.doc(params={'list_id': 'the id of the booklist', 'book_id' : 'the id of the book to be added'})
    @bklst.response(200, 'Success')
    @bklst.response(400, 'Bad request, invalid syntax')
    @bklst.response(404, 'Target book or book list not founded')
    def post(self, list_id, book_id):
        '''Add book to a certain book list'''
        book_list = BookListModel.find_by_id(list_id)
        if not book_list:
            return {'message' : 'book list {} not found'.format(list_id)}, 404
        book = BookModel.find_by_id(book_id)
        if not book:
            return {'message' : 'book {} not found'.format(book_id)}, 404
        assoc = ListBookAssociation.create_an_association(list_id, book_id)
        assoc.book = book
        assoc.list = book_list
        return book_list.json(), 200

@bklst.route('/remove_book_from_list/<int:list_id>/<int:book_id>')
class AddBookToABookList(Resource):

    @bklst.doc(params={'list_id': 'the id of the book list', 'book_id' : 'the id of the book to be added'})
    @bklst.response(200, 'Success')
    @bklst.response(400, 'Bad request, invalid syntax')
    @bklst.response(404, 'Target book or book list not founded')
    def delete(self, list_id, book_id):
        '''Remove book from a certain book list'''
        book_list = BookListModel.find_by_id(list_id)
        if not book_list:
            return {'message' : 'book list {} not found'.format(list_id)}, 404
        book = BookModel.find_by_id(book_id)
        if not book:
            return {'message' : 'book {} not found'.format(book_id)}, 404
        assoc = ListBookAssociation.find_by_id(list_id, book_id)
        if not assoc:
            return {'message' : 'book {} is not in this list'.format(book_id)}, 400
        ListBookAssociation.delete_from_db(assoc)
        return book_list.json(), 200

