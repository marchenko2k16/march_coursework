from dao.data import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2


class PostgresDb(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            try:
                connection = psycopg2.connect(host=host,
                                              database=database, user=username, password=password)
                cursor = connection.cursor()

                # execute a statement
                print('PostgreSQL database version:')
                cursor.execute('SELECT version()')

                # display the PostgreSQL database server version
                db_version = cursor.fetchone()
                print(db_version)

                engine = create_engine(DATABASE_URL)

                Session = sessionmaker(bind=engine)
                session = Session()

                PostgresDb._instance.connection = connection
                PostgresDb._instance.cursor = cursor
                PostgresDb._instance.sqlalchemy_session = session
                PostgresDb._instance.sqlalchemy_engine = engine

            except Exception as error:
                print('Error: connection not established {}'.format(error))

        return cls._instance