import psycopg2 as driver

from storage.exceptions import PostgresConnectionError

class PostgresBaseDriver:
    """General-purpose class for PostreSQL communication.

    Intended to be extended by other classes for more complex operations.

    Parameters
    ----------
    host: str
        The host where the Postgres server is running.
    port: int
        Port of the Postgres server.
    dbName: str
        Name of the database.
    user: str
        Username used at login.
    password:
        Password used at login.

    """
    def __enter__(self, host, port, dbName, user, password):
        self.host = host
        self.port = port
        self.dbName = dbName
        self.user=user
        self.password = password

        self._setup_connection()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def _setup_connection(self):
        """Tries to setup a connection"""
        try:
            self._conn = driver.connect(
                host=self.host,
                port=self.port,
                database=self.dbName,
                user=self.user,
                password=self.password,
            )
        except driver.driver.OperationalError or driver.DatabaseError:
            raise PostgresConnectionError(self.host, self.port, self.dbName)

        self._conn.autocommit = True

    def select(self, query, *args):
        with self._conn.cursor() as cursor:
            cursor.execute(query, args)
            results = cursor.fetchall()
            cursor.close()

        return results

    def insert_upload_delete(self, query, args):
        with self._conn.cursor() as cursor:
            cursor.execute(query, args)
            cursor.close()
        self._conn.commit()
