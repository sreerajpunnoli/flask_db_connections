from datetime import date

from marshmallow import exceptions, fields, validates, validates_schema
from marshmallow_enum import EnumField

from connections.extensions import ma
from connections.models.connection import Connection, ConnectionType
from connections.models.person import Person


class BaseModelSchema(ma.ModelSchema):
    def __init__(self, strict=True, **kwargs):
        super().__init__(strict=strict, **kwargs)


class PersonSchema(BaseModelSchema):
    email = fields.Email(required=True)
    date_of_birth = fields.Date(required=True)

    @validates('date_of_birth')
    def validate_date_of_birth(self, date_of_birth):
        if date_of_birth > date.today():
            raise exceptions.ValidationError('Cannot be in the future.')

    class Meta:
        model = Person


class ConnectionSchema(BaseModelSchema):
    from_person_id = fields.Integer()
    to_person_id = fields.Integer()
    connection_type = EnumField(ConnectionType, required=True)
    from_person = fields.Nested(PersonSchema, dump_only=True)
    to_person = fields.Nested(PersonSchema, dump_only=True)

    @validates_schema
    def validate_connection_type(self, connection):
        if 'connection_type' not in connection:
            return

        if connection['connection_type'] in [ConnectionType.son, ConnectionType.daughter]:
            from_person = Person.query.get(connection['from_person_id'])
            to_person = Person.query.get(connection['to_person_id'])
            if (from_person and to_person) and from_person.date_of_birth < to_person.date_of_birth:
                raise exceptions.ValidationError(
                    'Invalid connection - {} older than parent.'.format(
                        connection['connection_type'].value))
        elif connection['connection_type'] in [ConnectionType.father, ConnectionType.mother]:
            from_person = Person.query.get(connection['from_person_id'])
            to_person = Person.query.get(connection['to_person_id'])
            if (from_person and to_person) and from_person.date_of_birth > to_person.date_of_birth:
                raise exceptions.ValidationError(
                    'Invalid connection - {} younger than child.'.format(
                        connection['connection_type'].value))

    class Meta:
        model = Connection
