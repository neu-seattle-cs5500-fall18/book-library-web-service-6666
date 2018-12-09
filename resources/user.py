from flask_restplus import Resource, fields, Namespace
from models.book import  BookModel
from models.note import NoteModel
from models.user import UserModel


ur = Namespace('user', description='Book Loaner operations')


@ur.route('/<string:user_name>/<string:email>')
class AddUser(Resource):

    @ur.doc(params={'user_name' : 'the user name', 'email' : 'the email of the user'})
    @ur.response(200, 'Success')
    @ur.response(400, 'Bad request, invalid syntax')
    def post(self, user_name, email):
        '''Add a note to a certain book'''
        user = UserModel.create_new_user(user_name, email)
        return user.json(), 200


