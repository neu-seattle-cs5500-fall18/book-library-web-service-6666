from flask_restplus import Resource, fields, Namespace


bklst = Namespace('booklist', description='Booklist operations')


booklist_model = bklst.model('Booklist', {
   'id': fields.Integer(readOnly=True, description='The booklist id'),
   'name': fields.String(required=True, description='The booklist name'),
   'note': fields.String(description='Description of the booklist')
   })


booklists_db = []
first_booklist = {'bookId' : 1, 'name' : 'First Booklist', 'note' : 'first booklist'}
booklists_db.append(first_booklist)


@bklst.route('/<int:booklistId>')
class Booklist(Resource):
    '''Get a booklist by booklist id'''
    @bklst.doc(params={'booklistId' : 'a booklist id'})
    @bklst.response(200, 'Success')
    @bklst.response(400, 'Bad request, invalid syntax')
    @bklst.response(404, 'Booklist not found')
    def get(self, booklist_id):
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

    @bklst.doc(params={'booklistId' : 'the booklist id', 'name' : 'the booklist name', \
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
