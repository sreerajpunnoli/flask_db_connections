from connections.models.connection import Connection, ConnectionType

from marshmallow import exceptions


class Validate:
    
    def validate_create_connection(self, connection):
        existing_connection = Connection.query.filter_by(from_person_id=connection.from_person_id, \
                                                             to_person_id=connection.to_person_id, \
                                                             connection_type=connection.connection_type).first()
        if existing_connection:
            raise exceptions.ValidationError("Connection already exist.")
            
            
    def validate_modify_connection(self, connection_dict):
        print(2)
        if 'connection_type' not in connection_dict:
            print(3)
            raise exceptions.ValidationError("missing connection_type")
    
        conn_type = connection_dict['connection_type']
        if not ConnectionType.has_value(conn_type):
            print(4)
            raise exceptions.ValidationError(f"Invalid enum member {conn_type}")
            
# Singleton object
validate = Validate()