class PostgresConnectionError(Exception):
    def __init__(self, host, port, name, *args, **kwargs):
        super(PostgresConnectionError, self).__init__(
            self, 'Cannot connect to databae "{}" at {}:{}'.format(name, host,
                                                                   port),
            *args, **kwargs
        )
