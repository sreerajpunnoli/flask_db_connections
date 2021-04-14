from http import HTTPStatus

import pytest

from tests.factories import ConnectionFactory


def test_update_connection(db, testapp):
    connection = ConnectionFactory(connection_type='friend')
    db.session.commit()
    
    payload = {'connection_type': 'coworker'}
    res = testapp.patch(f'/connections/{connection.id}', json=payload)
    
    assert res.status_code == HTTPStatus.OK
    
    assert res.json is not None
    assert 'connection_type' in res.json
    assert 'coworker' == res.json['connection_type']


@pytest.mark.parametrize('connection_type_key, connection_type_value, connection_type_new_value, error_message', [
    pytest.param('connection_ty', 'friend', 'coworker', 'Missing data for required field.', id='missing connection type'),
    pytest.param('connection_type', 'friend', 'worker', 'Invalid enum member', id='Invalid connection type worker'),
    pytest.param('connection_type', 'brother', 'sis', 'Invalid enum member', id='Invalid connection type worker')
])
def test_update_connection_validations(db, testapp, connection_type_key, connection_type_value, \
                                                   connection_type_new_value, error_message):
    connection = ConnectionFactory(connection_type=connection_type_value)
    db.session.commit()
    
    # wrong key
    payload = {connection_type_key: connection_type_new_value}
    res = testapp.patch(f'/connections/{connection.id}', json=payload)
    
    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json['description'] == 'Input failed validation.'
    errors = res.json['errors']
    assert 'connection_type' in errors
    assert len(errors['connection_type']) == 1
    assert error_message in errors['connection_type'][0]
        