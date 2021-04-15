import enum

from connections.database import CreatedUpdatedMixin, CRUDMixin, db, Model


class ConnectionType(enum.Enum):
    mother = 'mother'
    father = 'father'
    son = 'son'
    daughter = 'daughter'
    husband = 'husband'
    wife = 'wife'
    brother = 'brother'
    sister = 'sister'
    friend = 'friend'
    coworker = 'coworker'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class Connection(Model, CRUDMixin, CreatedUpdatedMixin):
    id = db.Column(db.Integer, primary_key=True)
    from_person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    to_person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    connection_type = db.Column(db.Enum(ConnectionType), nullable=False)

    from_person = db.relationship('Person', foreign_keys=[from_person_id])
    to_person = db.relationship('Person', foreign_keys=[to_person_id])
