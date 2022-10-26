from sqlite_utils import Database
from config import VENDOR_DB_SCHEMA


class VendorDatabase():
    def __init__(self, db_file) -> None:
        self.database_file = db_file
        self._database = None

    @property
    def database(self):
        if self._database is None:
            self._database = Database(self.db_file)
        return self._database

    def create_table(self, VENDOR_DB_SCHEMA):
        self.database["vendors"].create(
            VENDOR_DB_SCHEMA,
            pk="id",
            transform=True)

    def insert_transaction(self, incoming_insert: dict):
        self.database["vendors"].upsert(
            incoming_insert,
            pk="id",
            transform=True)