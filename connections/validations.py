from marshmallow import exceptions

from connections.models.connection import Connection, ConnectionType


class Validate:

    def validate_create_connection(self, connection):
        existing_connection = Connection.query.filter_by(
                from_person_id=connection.from_person_id,
                to_person_id=connection.to_person_id,
                connection_type=connection.connection_type).first()
        if existing_connection:
            raise exceptions.ValidationError('Connection already exist.')

    def validate_modify_connection(self, connection_dict):
        if 'connection_type' not in connection_dict:
            raise exceptions.ValidationError('missing connection_type')

        conn_type = connection_dict['connection_type']
        if not ConnectionType.has_value(conn_type):
            raise exceptions.ValidationError(f'Invalid enum member {conn_type}')

    def validate_arguments(self, request_arguments, key):
        if key not in request_arguments:
            raise exceptions.ValidationError(f'Missing parameter {key}')

    def validate_person_object(self, person_object, id):
        if not person_object:
            raise exceptions.ValidationError(f'Invalid person with key {id}')


# Singleton object
validate = Validate()
