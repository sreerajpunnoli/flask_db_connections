from http import HTTPStatus

from tests.factories import ConnectionFactory

EXPECTED_FIELDS = [
    'id',
    'from_person',
    'to_person',
    'connection_type',
    'created_at',
    'updated_at'
]


def test_get_connections(db, testapp):
    ConnectionFactory.create_batch(10)
    db.session.commit()

    res = testapp.get('/connections')

    assert res.status_code == HTTPStatus.OK

    assert len(res.json) == 10
    for connection in res.json:
        for field in EXPECTED_FIELDS:
            assert field in connection
