from flask_restplus import Resource, Namespace
from models.note import NoteModel



nt = Namespace('note', description='Book Note operations')


@nt.route('/<int:book_id>/<string:content>')
class AddNote(Resource):

    @nt.doc(params={'book_id' : 'a book id', 'content' : 'the content of the note'})
    @nt.response(201, 'Success')
    @nt.response(400, 'Bad request, invalid syntax')
    def post(self, book_id, content):
        '''Add a note to a certain book'''
        try:
            note = NoteModel.create_note_for_book(book_id, content)
        except Exception as e:
            return {'message': 'no book found in this id'}, 404
        return note.json(), 201




@nt.route('/<int:book_id>')
class GetNotesForABook(Resource):

    @nt.doc(params={'book_id' : 'a book id'})
    @nt.response(200, 'Success')
    @nt.response(400, 'Bad request, invalid syntax')
    def get(self, book_id):
        '''Get the notes for a certain book'''
        try:
            notes = NoteModel.get_all_notes_for_book(book_id)
        except Exception as e:
            return {'message': 'no book found in this id'}, 404
        return [note.json() for note in notes], 200


@nt.route('/remove/<int:note_id>')
class RemoveNote(Resource):
    @nt.doc(params={'note_id': 'a note id'})
    @nt.response(200, 'Success')
    @nt.response(400, 'Bad request, invalid syntax')
    def delete(self, note_id):
        '''Remove a note for a certain book'''
        note = NoteModel.find_by_id(note_id)
        if not note:
            return {'message': 'no note found in this id'}, 404
        NoteModel.delete_from_db(note)
        return {'message': 'note {} has been removed.'.format(note_id)}, 200



@nt.route('/update/<int:note_id>/<string:new_content>')
class UpdateNote(Resource):
    @nt.doc(params={'note_id': 'a note id'})
    @nt.response(200, 'Success')
    @nt.response(400, 'Bad request, invalid syntax')
    def put(self, note_id, new_content):
        '''Update a note for a certain book'''
        try:
            note = NoteModel.update_note(note_id, new_content)
        except Exception as e:
            return {'message': 'no note found in this id'}, 404
        return note.json(), 200