import json
from functools import wraps
import flask
import util
from models.user import Person
from cassandra.cqlengine import connection
from flask import Blueprint, Response, request, render_template, redirect, url_for
from cassandra.auth import PlainTextAuthProvider

__author__="melek"
auth_provider = PlainTextAuthProvider(
        username='cassandra', password='cassandra')

api=Blueprint("api",__name__)

connection.setup(['10.0.0.60'], "flask_keyspace",protocol_version=4, retry_connect=True, auth_provider=auth_provider)


def json_api(f):
    @wraps(f)
    def decorted_function(*args , **kwargs):
        result = f(*args , **kwargs)
        json_result = util.to_json(result)
        return Response(response=json_result,
                        status=200,mimetype="application/json")
    return decorted_function

@api.route("/",defaults={"path":""})
@api.route('/<path:path>')
def default(path=None):
    return  "Denemelerrr"


@api.route("/add",methods=["POST"])
@json_api
def add_person():
    data=json.loads(flask.request.data)
    person=Person.create(email=data["email"])
    person.save()
    return  person.get_data()

@api.route("/get-all",methods=["GET"])
@json_api
def get_all():
    persons=Person.objects().all()
    return [person.get_data() for person in persons]


@api.route('/delete/<id>', methods=['DELETE'])
def delete__person(id):
    delete = Person.objects.get(id=id).delete()
    return '', 200


@api.route('/put/<id>', methods=['PUT'])
def update_Person(id):
 data = json.loads(flask.request.data)
 #body = request.get_json()
 Person.objects.get(id=id).update(**data)
 return '', 200

