from connections.database import CreatedUpdatedMixin, CRUDMixin, db, Model
from connections.models.connection import Connection, ConnectionType


class Person(Model, CRUDMixin, CreatedUpdatedMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(145), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    connections = db.relationship('Connection', foreign_keys='Connection.from_person_id')
    
    def mutual_friends(self, target):
        friend_connections = Connection.query.filter_by(from_person_id=self.id, \
                                    connection_type=ConnectionType.friend).distinct().all()
        friends = {Person.query.get(connection.to_person_id) for connection in friend_connections}

        target_connections = Connection.query.filter_by(from_person_id=target.id, \
                                    connection_type=ConnectionType.friend).distinct().all()
        target_friends = {Person.query.get(connection.to_person_id) for connection in target_connections}
        
        mutual_friends = friends.intersection(target_friends)
        
        return mutual_friends
