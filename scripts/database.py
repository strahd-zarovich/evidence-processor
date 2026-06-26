import pymysql

from common import get_config_value


class DatabaseError(Exception):
    pass


class Database:
    """
    Small MariaDB wrapper used by all Evidence Processor scripts.
    """

    def __init__(self, config: dict, logger=None):
        self.config = config
        self.logger = logger
        self.connection = None

    def connect(self):
        db = self.config.get("database", {})

        try:
            self.connection = pymysql.connect(
                host=get_config_value(self.config, "database.host", required=True),
                port=int(get_config_value(self.config, "database.port", 3306)),
                user=get_config_value(self.config, "database.username", required=True),
                password=get_config_value(self.config, "database.password", required=True),
                database=get_config_value(self.config, "database.name", required=True),
                charset=get_config_value(self.config, "database.charset", "utf8mb4"),
                connect_timeout=int(get_config_value(self.config, "database.connection_timeout", 10)),
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False,
            )

            if self.logger:
                self.logger.info("Connected to MariaDB host=%s database=%s", db.get("host"), db.get("database"))

            return self.connection

        except Exception as e:
            raise DatabaseError(f"Unable to connect to MariaDB: {e}") from e

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None

            if self.logger:
                self.logger.info("Disconnected from MariaDB")

    def ping(self):
        if not self.connection:
            raise DatabaseError("No active database connection")

        try:
            self.connection.ping(reconnect=False)
            return True
        except Exception as e:
            raise DatabaseError(f"MariaDB ping failed: {e}") from e

    def query_one(self, sql: str, params=None):
        if not self.connection:
            raise DatabaseError("No active database connection")

        with self.connection.cursor() as cursor:
            cursor.execute(sql, params or ())
            return cursor.fetchone()

    def query_all(self, sql: str, params=None):
        if not self.connection:
            raise DatabaseError("No active database connection")

        with self.connection.cursor() as cursor:
            cursor.execute(sql, params or ())
            return cursor.fetchall()

    def execute(self, sql: str, params=None):
        if not self.connection:
            raise DatabaseError("No active database connection")

        with self.connection.cursor() as cursor:
            cursor.execute(sql, params or ())
            return cursor.rowcount

    def commit(self):
        if self.connection:
            self.connection.commit()

    def rollback(self):
        if self.connection:
            self.connection.rollback()