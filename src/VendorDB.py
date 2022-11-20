from sqlite_utils import Database
from config import VENDOR_DATABASE_CONFIG
from typing import Union


def create_database(db_file: Union[str, bool]) -> Database:
    """Create an SQL Lite Database

    Args:
        db_file (Union[str,bool]): path of SQL DB file

    Returns:
        Database: Database class for use
    """

    if type(db_file) is bool:
        sql_database = Database(memory=True)
    else:
        sql_database = Database(self.database_file)

    return sql_database


class VendorDatabase():
    def __init__(self, db_file: Union[bool, str], db_config: dict) -> None:
        self._database = None
        self.config = db_config
        self.db_file = db_file

    @property
    def database(self) -> Database:
        if self._database is None:
            self._database = create_database(self.db_file)
        return self._database

    def get_vendor(self, vendor_id: str):
        return self.database['vendors'].get(vendor_id)

    def create_table(self):
        self.database[self.config['table_name']].create(
            self.config['table_schema'],
            pk="id")

    def insert_transaction(self, incoming_insert: dict):
        self.database["vendors"].upsert(
            incoming_insert,
            pk="id")


if __name__ == "__main__":
    db = VendorDatabase(
        db_file="test.db",
        db_config=VENDOR_DATABASE_CONFIG)
    db.insert_transaction(
        {
            "id": "Youtube",
            "duration": 200
        }
    )
    print(db.get_vendor(vendor_id='Youtube'))
