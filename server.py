import random
import string

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

Persons_dict = {
    "1": {'name': 'Aravind', 'domain': 'Web App'},
    "2": {'name': 'Sandeep', 'domain': 'ML+DevOps'},
    "3": {'name': 'Karthik', 'domain': 'Arduino'},
}

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('domain')

# 404 -> Not found


def abort_if_person_doesnt_exist(id):
    if id not in Persons_dict:
        abort(404, message="Person {} doesn't exist".format(id))


def abort_if_person_exists(id):
    if id in Persons_dict:
        abort(404, message="Person {} already exists".format(id))


class Persons(Resource):
    def get(self):
        return Persons_dict

    def post(self):
        args = parser.parse_args()
        id = str(len(Persons_dict) + 1)
        abort_if_person_exists(id)
        Persons_dict[id] = args
        # 201 -> created
        return {'id': id}, 201


class Person(Resource):
    def get(self, id):
        # print(type(id))
        # print(Persons_dict)
        abort_if_person_doesnt_exist(id)
        return {id: Persons_dict[id]}


api.add_resource(Persons, '/persons')
api.add_resource(Person, '/person/<id>')


@app.route('/')
def index():
    return 'OK!'


if __name__ == '__main__':
    app.run()
