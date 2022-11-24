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
        sql_database = Database(db_file)

    return sql_database


class VendorDatabase():
    def __init__(self, db_file: Union[bool, str] = None) -> None:
        self._database = None
        self.config = VENDOR_DATABASE_CONFIG
        if not db_file:
            self.db_file = VENDOR_DATABASE_CONFIG['db_file']

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
        
    def get_all_durations(self):
        for record in self.database.query("select duration from vendors"):
            yield record['duration']


if __name__ == "__main__":
    db = VendorDatabase()
    db.insert_transaction(
        {
            "id": "Youtube",
            "duration": 200
        }
    )
    db.insert_transaction(
        {
            "id": "Spotify",
            "duration": 200
        }
    )
    db.insert_transaction(
        {
            "id": "Youtube",
            "duration": 200
        }
    )
    db.insert_transaction(
        {
            "id": "Aggregated Platforms",
            "duration": 200
        }
    )
    for duration in db.get_all_durations():
        print(duration)
