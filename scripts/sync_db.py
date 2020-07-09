from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table


from models.user import Person


__author__="melek"

auth_provider = PlainTextAuthProvider(
        username='cassandra', password='cassandra')

connection.setup(['localhost'],
                 protocol_version=4, retry_connect=True, auth_provider=auth_provider)

sync_table(Person)

