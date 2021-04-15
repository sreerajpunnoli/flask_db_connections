from http import HTTPStatus

from flask import Blueprint, request
from webargs.flaskparser import use_args

from connections.models.person import Person
from connections.models.connection import Connection
from connections.schemas import ConnectionSchema, PersonSchema
from connections.validations import validate

blueprint = Blueprint('connections', __name__)


@blueprint.route('/people', methods=['GET'])
def get_people():
    people_schema = PersonSchema(many=True)
    people = Person.query.all()
    return people_schema.jsonify(people), HTTPStatus.OK


@blueprint.route('/people', methods=['POST'])
@use_args(PersonSchema(), locations=('json',))
def create_person(person):
    person.save()
    return PersonSchema().jsonify(person), HTTPStatus.CREATED


@blueprint.route('/people/<int:id>/mutual_friends', methods=['GET'])
def get_mutual_friends(id):
    validate.validate_arguments(request.args, 'target_id')
    target_id = request.args.get('target_id')
    
    person = Person.query.get(id)
    validate.validate_person_object(person, id)
    
    target_person = Person.query.get(target_id)
    validate.validate_person_object(target_person, target_id)
    
    mutual_friends = person.mutual_friends(target_person)
    
    person_schema = PersonSchema(many=True)
    return person_schema.jsonify(mutual_friends), HTTPStatus.OK


@blueprint.route('/connections', methods=['GET'])
def get_connections():
    connection_schema = ConnectionSchema(many=True)
    connections = Connection.query.all()
    return connection_schema.jsonify(connections), HTTPStatus.OK


@blueprint.route('/connections/<int:id>', methods=['PATCH'])
@use_args(ConnectionSchema(), locations=('json',))
def modify_connection(connection, id):
    connection_dict = request.json
    validate.validate_modify_connection(connection_dict)
    
    saved_connection = Connection.query.get(id)
    connection = saved_connection.update(**connection_dict)
    
    return ConnectionSchema().jsonify(connection), HTTPStatus.OK


@blueprint.route('/connections', methods=['POST'])
@use_args(ConnectionSchema(), locations=('json',))
def create_connection(connection):
    validate.validate_create_connection(connection)
            
    connection.save()
    return ConnectionSchema().jsonify(connection), HTTPStatus.CREATED
