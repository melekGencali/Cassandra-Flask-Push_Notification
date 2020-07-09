from cassandra.auth import PlainTextAuthProvider
from models.base import Base
from  cassandra.cqlengine import columns
import uuid
from cassandra.cqlengine import connection
__author__="melek"


auth_provider = PlainTextAuthProvider(
        username='cassandra', password='cassandra')

connection.setup(['localhost'], "flask_keyspace",protocol_version=4,
                 retry_connect=True, auth_provider=auth_provider)

class Person(Base):
    id= columns.UUID(primary_key=True,default=uuid.uuid4)
    email=columns.Text()


    def get_data(self):
        return {
            "id": str(self.id),
            "email": self.email
        }

