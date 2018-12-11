from flask_restplus import Resource, Namespace
from models.book import BookModel
from models.author import AuthorModel
from models.genre import GenreModel

from datetime import datetime

bk = Namespace('book', description='Book Library operations')


@bk.route('/add-book/<string:title>/<string:author>/<string:date>/<string:genre>')
class AddANewBook(Resource):
    @bk.doc(params={'title' : 'a book title', 'author' : 'the book author', \
                    'date' : 'book release date', 'genre': 'subject of the book'})
    @bk.response(201, 'Book successful added')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(403, 'Can not add the book')
    def post(self, title, author, date, genre):
        '''Add a new book'''
        cur_author = AuthorModel.search_and_add_author(author)

        cur_genre = GenreModel.search_and_add_genre(genre)

        release_date = DateRead.read_date(date)

        #create the new book, add into db
        new_book = BookModel(title, cur_author.id, release_date, cur_genre)
        new_book.save_to_db()

        if not new_book:
            return {"message" : "add book error"}, 403
        return new_book.json(), 201




@bk.route('/remove-book/<int:book_id>')
class RemoveById(Resource):
    @bk.doc(params={'book_id' : 'a book id'})
    @bk.response(200, 'Book successfully removed')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(404, 'Book not found')
    def delete(self, book_id):
        '''Remove a book by book id'''
        book = BookModel.find_by_id(book_id)
        if book:
            BookModel.delete_from_db(book)
            return {'message' : 'book with id {} has been removed.'.format(book_id)}, 200
        return {'message' : 'book with id {} is not found.'.format(book_id)}, 404



@bk.route('/update-book/<int:book_id>/<string:author>/<string:title>/<string:date>/<string:genre>')
class UpdateById(Resource):
    @bk.doc(params={'book_id':'a book id', 'author':'book author name', 'title':'book title', \
                    'date':'book release date', 'genre':'subject of the book'})
    @bk.response(200, 'Book successfully updated')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(404, 'Book not found')
    def put(self, book_id, author, title, date, genre):
        '''Update a book by book id'''
        cur_book = BookModel.find_by_id(book_id)

        if not cur_book:
            return {'message' : 'book with id {} is not found.'.format(book_id)}, 404

        new_author = AuthorModel.search_and_add_author(author)
        new_genre = GenreModel.search_and_add_genre(genre)
        new_date = DateRead.read_date(date)

        cur_book = BookModel.update_book(book_id, title, new_author, new_date, new_genre)
        return cur_book.json(), 200


@bk.route('/all-books')
class GetAllBooks(Resource):
    def get(self):
        '''Display all the books'''
        return [book.json() for book in BookModel.find_all()], 200



@bk.route('/search-by-author/<string:author_name>')
class SearchByAuthorName(Resource):

    @bk.doc(params={'author_name' : 'Author name'})
    @bk.response(200, 'Success')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(404, 'No author found with the given author id')
    def get(self, author_name):
        '''Get books by author id'''
        author = AuthorModel.find_by_name(author_name)
        if not author:
            return [], 404
        try:
            books = AuthorModel.get_all_books_from_author(author.id)
        except Exception as e:
            return [], 404
        book_list = [book.json() for book in books]

        return book_list, 200



@bk.route('/search-by-date-range/<string:start_date>/<string:end_date>')
class SearchByDateRange(Resource):

    @bk.doc(params={'start_date' : 'Start date of the search range', "end_date" \
    : "End date of the search range"})
    @bk.response(200, 'Success')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(404, 'No books found within the given date interval')
    def get(self, start_date, end_date):
        '''Get books by start date and end date'''
        start = DateRead.read_date(start_date)
        end = DateRead.read_date(end_date)

        books = BookModel.find_by_date_range(start, end)
        book_list = [book.json() for book in books]
        return book_list, 200




@bk.route('/search_by_title/<string:title>')
class SearchByTitle(Resource):

    @bk.doc(params={'title' : 'a book title'})
    @bk.response(200, 'Success')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(404, 'Book not found')
    def get(self, title):
        '''Search a book by book title'''
        try:
            books = BookModel.find_by_name(title)
        except Exception as e:
            return [], 404
        book_list = [book.json() for book in books]
        return book_list, 200



@bk.route('/search_by_genre/<string:genre>')
class SearchByGenre(Resource):

    @bk.doc(params={'genre' : 'a book genre'})
    @bk.response(200, 'Success')
    @bk.response(400, 'Bad request, invalid syntax')
    @bk.response(404, 'Genre not found')
    def get(self, genre):
        '''Get books on a certain genre'''
        try:
            books = GenreModel.get_all_books_from_genre(genre)
        except Exception as e:
            return [], 404
        book_list = [book.json() for book in books]

        return book_list, 200


@bk.route('/advanced_search/<string:author>/<string:genre>/<string:start_date>/<string:end_date>')
class AdvancedSearch(Resource):
    @bk.doc(params={'author' : 'author name', 'genre' : 'genre or subject of a book',\
                    'start_date' : 'start date range', 'end_date' : 'end date range'})
    @bk.response(200, 'Success')
    @bk.response(400, 'Bad request, invalid syntax')
    def get(self, author, genre, start_date, end_date):
        '''Search books by multiple requirements'''
        search_by_author_res = SearchByAuthorName().get(author)[0]
        search_by_genre_res = SearchByGenre().get(genre)[0]
        search_by_date_res = SearchByDateRange().get(start_date, end_date)[0]
        temp = [book for book in search_by_date_res if book in search_by_genre_res]
        res = [book for book in temp if book in search_by_author_res]
        return res, 200



class DateRead:
    @staticmethod
    def read_date(date_str):
        return datetime(int(date_str[0:4]), int(date_str[4:6]), int(date_str[6:8])).date()

