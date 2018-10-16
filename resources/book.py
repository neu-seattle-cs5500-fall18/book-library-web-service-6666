from flask_restplus import Resource, fields, Namespace


bk = Namespace('book', description='Book Library operations')


book_model = bk.model('Book', {
    'id': fields.Integer(readOnly=True, description='The book id'),
    'title': fields.String(required=True, description='The book title'),
    'note': fields.String(description='Note of the book'),
    'authorId': fields.Integer(required=True, description='The author id of the bookd'),
    'date' : fields.String(description='Date of book release'),
    'genre': fields.String(description='Genre of the book')
})


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
    @bk.doc(params={'bookId' : 'a book id'})
    @bk.response(200, 'Book successfully removed')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(404, 'Book not found')
    def delete(self, id):
        '''Remove a book by book id'''
        return {'message' : 'book {} has been removed.'}.format(id), 200



@bk.route('/update-book/<int:bookId>/update?authorId=<string:authorId>\
&title=<string:title>&note=<string:note>&date=<string:date>')
class Update_by_id(Resource):
    @bk.doc(params={'bookId' : 'a book id', 'authorId' : 'book author id', 'title' \
    : 'book title', 'note' : 'book note', 'date' : 'book release date'})
    @bk.response(200, 'Book successfully updated')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(404, 'Book not found')
    def post(self, book_id, author_id, title, note, date):
        '''Update a book by book id'''
        return {'message' : 'book {} has been updated.'}.format(id), 200



@bk.route('/search-by-author/search?authorId=<int:authorId>')
class Search_by_author_id(Resource):

    @bk.doc(params={'authorId' : 'Author ID'})
    @bk.response(200, 'Success')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(404, 'No author found with the given author id')
    @bk.marshal_with(book_model, as_list=True)
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
    @bk.marshal_with(book_model, as_list=True)
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
    @bk.marshal_with(book_model, as_list=True)
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







@bk.route('/update-book-note/<int:bookId>')
class Book_note(Resource):
    '''the note of a given book'''
    @bk.doc(params={'bookId' : 'a book id'})
    @bk.response(200, 'Success')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(404, 'No book found')
    def get(self, bookId):
        '''Get the note of a book'''
        return {'message' : 'book note found'}, 200

    @bk.doc(params={'bookId' : 'a book id', 'note' : 'note for a book'})
    @bk.response(200, 'Success')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(404, 'No book found')
    def put(self, bookId, note):
        '''Update a book note'''
        return {'message' : 'book {} has been updated.'}.format(id), 200



    @bk.doc(params={'bookId' : 'a book id'})
    @bk.response(200, 'Success')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(404, 'No book found')
    def delete(self, bookId, note):
        '''Delete the note for a book'''
        return {'message' : 'the note of book {} has been deleted.'}.format(id), 200
