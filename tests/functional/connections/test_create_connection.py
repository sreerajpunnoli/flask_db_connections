from datetime import date
from http import HTTPStatus

from tests.factories import PersonFactory

from connections.models.connection import Connection


def test_can_create_connection(db, testapp):
    person_from = PersonFactory(first_name='Jim')
    person_to = PersonFactory(first_name='Dwight')
    db.session.commit()
    payload = {
        'from_person_id': person_from.id,
        'to_person_id': person_to.id,
        'connection_type': 'coworker',
    }
    res = testapp.post('/connections', json=payload)

    assert res.status_code == HTTPStatus.CREATED

    assert 'id' in res.json

    connection = Connection.query.get(res.json['id'])

    assert connection is not None
    assert connection.from_person_id == person_from.id
    assert connection.to_person_id == person_to.id
    assert connection.connection_type.value == 'coworker'


def test_create_connection_parent_and_child_validation(db, testapp):
    parent = PersonFactory(date_of_birth=date(1950, 10, 1))
    child = PersonFactory(date_of_birth=date(1990, 10, 1))
    db.session.commit()
    # Child is son to parent
    payload = {
        'from_person_id': child.id,
        'to_person_id': parent.id,
        'connection_type': 'son',
    }
    res = testapp.post('/connections', json=payload)

    assert res.status_code == HTTPStatus.CREATED

    assert 'id' in res.json

    connection = Connection.query.get(res.json['id'])

    assert connection is not None
    assert connection.from_person_id == child.id
    assert connection.to_person_id == parent.id
    assert connection.connection_type.value == 'son'


def test_create_connection_duplicate_validation(db, testapp):
    parent = PersonFactory(date_of_birth=date(1950, 10, 1))
    child = PersonFactory(date_of_birth=date(1990, 10, 1))
    db.session.commit()
    # Child is son to parent
    payload = {
        'from_person_id': child.id,
        'to_person_id': parent.id,
        'connection_type': 'son',
    }
    res = testapp.post('/connections', json=payload)

    assert res.status_code == HTTPStatus.CREATED

    assert 'id' in res.json

    connection = Connection.query.get(res.json['id'])

    assert connection is not None
    assert connection.from_person_id == child.id
    assert connection.to_person_id == parent.id
    assert connection.connection_type.value == 'son'
    
    # Try to create connection with same payload once again
    res = testapp.post('/connections', json=payload)
    
    assert res.status_code == HTTPStatus.BAD_REQUEST
    
    assert 'description' in res.json
    assert 'Input failed validation.' == res.json['description']
    assert 'errors' in res.json
    assert '_schema' in res.json['errors']
    error_messages = res.json['errors']['_schema']
    assert len(error_messages) == 1
    assert 'Connection already exist.' == error_messages[0]
    
    
    
    
