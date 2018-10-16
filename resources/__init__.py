from flask_restplus import Api, Resource, fields

from .book import bk as book_api
from .booklist import bklst as booklist_api
from .loanrec import loanrec as loan_record_api

api = Api(version='1.0', title='Book Library API',
    description='Book Library API From Team 6666',
)

api.add_namespace(book_api)
api.add_namespace(booklist_api)
api.add_namespace(loan_record_api)
