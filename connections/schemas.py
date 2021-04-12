from marshmallow import fields, exceptions
from marshmallow_enum import EnumField

from connections.extensions import ma
from connections.models.connection import Connection, ConnectionType
from connections.models.person import Person

from datetime import date


class BaseModelSchema(ma.ModelSchema):
    def __init__(self, strict=True, **kwargs):
        super().__init__(strict=strict, **kwargs)


class PersonSchema(BaseModelSchema):
    
    def validate_dob(dob):
        if dob > date.today():
            raise exceptions.ValidationError('Cannot be in the future.')
                          
    date_of_birth = fields.Date(required=True, validate=validate_dob)
    email = fields.Email(required=True)

    class Meta:
        model = Person


class ConnectionSchema(BaseModelSchema):
    from_person_id = fields.Integer()
    to_person_id = fields.Integer()
    connection_type = EnumField(ConnectionType)

    class Meta:
        model = Connection
        
