from http import HTTPStatus

from tests.factories import PersonFactory, ConnectionFactory

EXPECTED_FIELDS = [
    'id',
    'first_name',
    'last_name',
    'email',
]


def create_friends():
    person = PersonFactory()
    target_person = PersonFactory()

    # some decoy connections (not mutual)
    ConnectionFactory.create_batch(2, to_person=person)
    ConnectionFactory.create_batch(2, to_person=target_person)

    mutual_friends = PersonFactory.create_batch(3)
    for f in mutual_friends:
        ConnectionFactory(from_person=person, to_person=f, connection_type='friend')
        ConnectionFactory(from_person=target_person, to_person=f, connection_type='friend')

    # mutual connections, but not friends
    decoy = PersonFactory()
    ConnectionFactory(from_person=person, to_person=decoy, connection_type='coworker')
    ConnectionFactory(from_person=target_person, to_person=decoy, connection_type='coworker')
    
    return person, target_person, mutual_friends


def create_friends_without_decoy():
    person = PersonFactory()
    target_person = PersonFactory()

    mutual_friends = PersonFactory.create_batch(3)
    for f in mutual_friends:
        ConnectionFactory(from_person=person, to_person=f, connection_type='friend')
        ConnectionFactory(from_person=target_person, to_person=f, connection_type='friend')
    
    return person, target_person, mutual_friends
    

def check_mutual_friends(res, mutual_friends):
    expected_mutual_friend_ids = [f.id for f in mutual_friends]
    
    assert res.status_code == HTTPStatus.OK

    assert len(res.json) == 3
    for f in res.json:
        for field in EXPECTED_FIELDS:
            assert field in f
        assert f['id'] in expected_mutual_friend_ids


def test_can_get_mutual_friends(db, testapp):
    person, target_person, mutual_friends = create_friends()
    db.session.commit()
    
    res = testapp.get(f'/people/{person.id}/mutual_friends?target_id={target_person.id}')

    check_mutual_friends(res, mutual_friends)


def test_mutual_frieds_after_swapping(db, testapp):
    person, target_person, mutual_friends = create_friends_without_decoy()
    db.session.commit()
    
    res = testapp.get(f'/people/{person.id}/mutual_friends?target_id={target_person.id}')
    # get mutual friends after swapping person and target_person
    swapped_res = testapp.get(f'/people/{target_person.id}/mutual_friends?target_id={person.id}')
    
    check_mutual_friends(res, mutual_friends)
    check_mutual_friends(swapped_res, mutual_friends)
    
    assert res.json == swapped_res.json


def test_mutual_friends_invalid_person(db, testapp):
    person, target_person, mutual_friends = create_friends_without_decoy()
    db.session.commit()
    
    available_person_ids = [f.id for f in mutual_friends + [person, target_person]]
    
    invalid_person_id = max(available_person_ids) + 1
    
    res = testapp.get(f'/people/{person.id}/mutual_friends?target_id={invalid_person_id}')

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json['description'] == 'Input failed validation.'
    
    errors = res.json['errors']
    assert len(errors) == 1
    
    assert f'Invalid person with key {invalid_person_id}' in errors[0]
    