from cassandra.cqlengine.models import Model

__author__="melek"



class Base(Model):
    __abstract__ = True
    __keyspace__ = "flask_keyspace"